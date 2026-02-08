"""
Agent Service - OpenAI GPT Integration with Function Calling

Manages OpenAI agent initialization, tool execution, and conversation management.
Implements stateless agent pattern with database-persisted conversation history.
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.services.conversation_service import ConversationService
from src.models.message import MessageRole
from mcp_tools.task_tools import get_all_tools
from mcp_tools.task_tools_db import execute_tool_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentService:
    """Service for OpenAI GPT agent operations with function calling."""

    SYSTEM_PROMPT = """You are a helpful AI assistant for task management. You help users:
- Create new tasks from natural language descriptions
- View and filter their task lists
- Update task status (complete/pending)
- Delete tasks
- Get productivity insights and statistics

You have access to these tools:
1. add_task(title, description?) - Create a new task
2. get_tasks(status?) - Get tasks (filter by 'pending' or 'completed')
3. update_task_status(task_id, status) - Update task status
4. delete_task(task_id) - Delete a task
5. get_task_statistics() - Get productivity stats

**Task Creation Guidelines:**
- When users say "Add a task to [action]", extract the action as the title
- For compound requests like "Add buy milk, call dentist, and finish report", create multiple tasks
- If input is ambiguous (e.g., just "milk"), ask clarifying questions
- After creating a task, respond with: "Added task: {title}"

**Task Retrieval Guidelines:**
- When users ask "What's pending?" or "Show pending tasks", call get_tasks with status="pending"
- When users ask "What have I completed?", call get_tasks with status="completed"
- When users ask "Show my tasks" or "List all tasks", call get_tasks without status parameter
- Format task lists as numbered lists with task IDs, titles, and status

**Task Status Update Guidelines:**
- When users say "Mark [task name] as done/complete", first call get_tasks to find the task by title, then call update_task_status
- Support fuzzy matching for task titles

**Task Deletion Guidelines:**
- When users say "Delete [task name]", first call get_tasks to find the task, then call delete_task
- For bulk deletion, ask for confirmation first

**Task Analytics Guidelines:**
- When users ask "How am I doing?" or "Show my stats", call get_task_statistics
- Format statistics clearly with percentages and counts

Be concise, friendly, and use emojis appropriately. Always confirm actions clearly."""

    @staticmethod
    def _get_openai_client():
        """Get OpenAI client instance."""
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or api_key == "your-openai-api-key-here":
                return None
            return OpenAI(api_key=api_key)
        except ImportError:
            logger.error("OpenAI SDK not installed")
            return None

    @staticmethod
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type(Exception)
    )
    async def get_agent_response(
        session: AsyncSession,
        user_id: str,
        user_message: str,
        conversation_id: Optional[int] = None
    ) -> Tuple[str, int, List[str]]:
        """
        Get response from OpenAI GPT agent with function calling.

        Args:
            session: Database session
            user_id: User identifier
            user_message: User's message
            conversation_id: Optional existing conversation ID

        Returns:
            Tuple of (response_text, conversation_id, tools_used)
        """
        logger.info(f"Agent request: user_id={user_id} | conversation_id={conversation_id} | message='{user_message[:50]}...'")

        # Get or create conversation
        conversation = await ConversationService.get_or_create_conversation(
            session, user_id, conversation_id
        )

        # Get conversation history (last 50 messages)
        history = await ConversationService.get_conversation_history(
            session, conversation.id, user_id
        )

        # Convert to OpenAI message format
        messages = [{"role": "system", "content": AgentService.SYSTEM_PROMPT}]

        for msg in history:
            messages.append({
                "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                "content": msg.content
            })

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Save user message to database
        await ConversationService.add_message(
            session, conversation.id, user_id,
            MessageRole.USER, user_message
        )

        # Get OpenAI client
        client = AgentService._get_openai_client()
        if not client:
            response_text = AgentService._get_fallback_response(user_message)
            tools_used = []

            await ConversationService.add_message(
                session, conversation.id, user_id,
                MessageRole.ASSISTANT, response_text
            )
            await session.commit()

            return (response_text, conversation.id, tools_used)

        # Call OpenAI with function calling
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        tools = get_all_tools()
        tools_used = []

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            # Process tool calls in loop
            while message.tool_calls:
                # Add assistant message with tool calls to conversation
                messages.append({
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })

                # Execute each tool call
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_input = json.loads(tool_call.function.arguments)
                    tools_used.append(tool_name)

                    logger.info(f"Tool invocation: {tool_name} | params={tool_input}")

                    # Execute tool with database session
                    tool_result = await execute_tool_db(session, tool_name, tool_input, user_id)

                    logger.info(f"Tool result: {tool_name} | success={tool_result.get('success')}")

                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })

                # Continue conversation with tool results
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto"
                )

                message = response.choices[0].message

            # Extract final text response
            response_text = message.content or ""

            # Save assistant response to database
            await ConversationService.add_message(
                session, conversation.id, user_id,
                MessageRole.ASSISTANT, response_text
            )

            await session.commit()

            logger.info(f"Agent response: conversation_id={conversation.id} | tools_used={tools_used} | response_length={len(response_text)}")

            return (response_text, conversation.id, tools_used)

        except Exception as e:
            logger.error(f"Agent error: {str(e)}")
            await session.rollback()

            error_response = f"I'm experiencing technical difficulties. Error: {str(e)[:100]}"

            try:
                await ConversationService.add_message(
                    session, conversation.id, user_id,
                    MessageRole.ASSISTANT, error_response
                )
                await session.commit()
            except:
                pass

            return (error_response, conversation.id, [])

    @staticmethod
    def _get_fallback_response(user_message: str) -> str:
        """Get fallback response when API is not configured."""
        if any(word in user_message.lower() for word in ["add", "create", "new task"]):
            return """I can help you create tasks!

**To activate AI capabilities:**

1. Get your OpenAI API key from: https://platform.openai.com/api-keys
2. Add it to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Restart the server

Once configured, I'll be able to actually create, update, and manage your tasks!"""

        elif "help" in user_message.lower():
            return """**AI Todo Chatbot with Tools**

**Status**: Running in demo mode (OpenAI API not configured)

**What I can do (once API key is added)**:
- Create tasks: "Add a task to buy groceries"
- View tasks: "Show my pending tasks"
- Update tasks: "Mark buy groceries as done"
- Delete tasks: "Delete the groceries task"
- Get stats: "How am I doing today?"

**Setup**: Add OPENAI_API_KEY to backend/.env and restart server."""

        else:
            return f'Message received: "{user_message}"\n\nOpenAI API not configured. Add OPENAI_API_KEY to backend/.env to enable AI features. Type "help" for more info.'
