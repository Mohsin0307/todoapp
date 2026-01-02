"""
Agent Service - Claude AI Integration with Tool Use

Manages Claude AI agent initialization, tool execution, and conversation management.
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentService:
    """Service for Claude AI agent operations with tool use."""

    # System prompt for task management agent
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

Be concise, friendly, and use emojis appropriately. When users ask about tasks, use the appropriate tools to retrieve or modify data. Always confirm actions and provide helpful feedback.

When a task is created, updated, or deleted, confirm the action clearly. When listing tasks, format them in a readable way with numbers. Be conversational and helpful!"""

    @staticmethod
    def _get_anthropic_client():
        """Get Anthropic client instance."""
        try:
            from anthropic import Anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key or api_key.startswith("sk-ant-api03-xxx"):
                return None
            return Anthropic(api_key=api_key, default_headers={})
        except ImportError:
            logger.error("Anthropic SDK not installed")
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
        Get response from Claude AI agent with tool execution.

        Args:
            session: Database session
            user_id: User identifier
            user_message: User's message
            conversation_id: Optional existing conversation ID

        Returns:
            Tuple of (response_text, conversation_id, tools_used)

        Raises:
            Exception: If API key not configured or API call fails
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

        # Convert to Claude format
        messages = ConversationService.messages_to_claude_format(history)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Save user message to database
        await ConversationService.add_message(
            session, conversation.id, user_id,
            MessageRole.USER, user_message
        )

        # Get Anthropic client
        client = AgentService._get_anthropic_client()
        if not client:
            # API not configured - return helpful message
            response_text = AgentService._get_fallback_response(user_message)
            tools_used = []

            # Save assistant response
            await ConversationService.add_message(
                session, conversation.id, user_id,
                MessageRole.ASSISTANT, response_text
            )
            await session.commit()

            return (response_text, conversation.id, tools_used)

        # Call Claude AI with tools
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "2048"))
        tools = get_all_tools()
        tools_used = []

        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=AgentService.SYSTEM_PROMPT,
                tools=tools,
                messages=messages
            )

            # Process tool calls in loop
            while response.stop_reason == "tool_use":
                # Extract tool use block
                tool_use_block = None
                for block in response.content:
                    if block.type == "tool_use":
                        tool_use_block = block
                        break

                if not tool_use_block:
                    break

                tool_name = tool_use_block.name
                tool_input = tool_use_block.input
                tools_used.append(tool_name)

                logger.info(f"Tool invocation: {tool_name} | params={tool_input}")

                # Execute tool with database session
                tool_result = await execute_tool_db(session, tool_name, tool_input, user_id)

                logger.info(f"Tool result: {tool_name} | success={tool_result.get('success')}")

                # Add assistant's tool use to conversation
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Add tool result
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": json.dumps(tool_result)
                    }]
                })

                # Continue conversation with tool result
                response = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    system=AgentService.SYSTEM_PROMPT,
                    tools=tools,
                    messages=messages
                )

            # Extract final text response
            response_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    response_text += block.text

            # Save assistant response to database
            await ConversationService.add_message(
                session, conversation.id, user_id,
                MessageRole.ASSISTANT, response_text
            )

            # Commit all changes
            await session.commit()

            logger.info(f"Agent response: conversation_id={conversation.id} | tools_used={tools_used} | response_length={len(response_text)}")

            return (response_text, conversation.id, tools_used)

        except Exception as e:
            logger.error(f"Agent error: {str(e)}")
            await session.rollback()

            # Return error message
            error_response = f"❌ I'm experiencing technical difficulties. Error: {str(e)[:100]}"

            # Try to save error message
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
            return """✅ I can help you create tasks!

**To activate Claude AI with tool capabilities:**

1. Get your Anthropic API key from: https://console.anthropic.com/settings/keys
2. Add it to `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ```
3. Restart the server

Once configured, I'll be able to actually create, update, and manage your tasks!"""

        elif "help" in user_message.lower():
            return """🤖 **Claude AI Todo Chatbot with Tools**

**Status**: Running in demo mode (Claude API not configured)

**What I can do (once API key is added)**:
- ✅ Create tasks: "Add a task to buy groceries"
- ✅ View tasks: "Show my pending tasks"
- ✅ Update tasks: "Mark buy groceries as done"
- ✅ Delete tasks: "Delete the groceries task"
- ✅ Get stats: "How am I doing today?"

**Available Tools**:
1. add_task - Create new tasks
2. get_tasks - View your task list
3. update_task_status - Mark tasks complete/pending
4. delete_task - Remove tasks
5. get_task_statistics - View productivity insights

**Setup**: Add ANTHROPIC_API_KEY to backend/.env and restart server."""

        else:
            return f'💬 Message received: "{user_message}"\n\n⚠️ Claude API not configured. Add ANTHROPIC_API_KEY to backend/.env to enable AI features. Type "help" for more info.'
