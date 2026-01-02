---
name: agent-architect
description: Design focused sub-agents with clear roles, scopes, and prompts for complex projects.
version: 1.0
---

## When to Use
- When a project is too large for a single agent
- When frontend, backend, AI, or security work should be isolated
- When using Claude sub-agents (wshobson/agents pattern)
- To reduce token usage and cognitive overload

## Procedure
1. Analyze the project scope and architecture
2. Identify clear responsibility boundaries
3. Define one agent per responsibility
4. Write a concise system prompt for each agent
5. Explicitly define:
   - What the agent CAN do
   - What the agent MUST NOT do
6. Keep agents narrowly focused

## Output Format
For each agent:
- Agent Name
- Role / Responsibility
- Allowed Tasks
- Forbidden Tasks
- System Prompt (ready to use)

## Recommended Agents
- Frontend Agent (UI, UX, components)
- Backend Agent (APIs, database, logic)
- AI Agent (chat, tools, MCP, prompts)
- Security Agent (auth, validation, risks)
- Docs Agent (README, specs, architecture)

## Constraints
- Agents must not overlap responsibilities
- Avoid general-purpose agents
- Optimize for reuse across phases
