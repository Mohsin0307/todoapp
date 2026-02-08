# Agent Responsibilities and Communication Flows

## Agent Responsibilities

### Main Infrastructure Agent
- Overall orchestration of the deployment process
- Coordination between sub-agents
- High-level decision making
- Status reporting and validation

### Planner Agent
- Integration with sp.plan functionality
- Generation of implementation plans that comply with constitutional principles
- Feature specification parsing
- Plan validation and constitution compliance verification

### Executor Agent
- Execution of tasks according to specifications provided by the planner agent
- Carrying out planned actions
- Reporting completion status
- Managing task entity handling

### Reviewer Agent
- Validation of completed tasks
- Providing approval or rejection feedback
- Generating validation results
- Quality assurance of completed work

## Communication Flows

### 1. Planning Flow
Planner Agent ↔ Main Infrastructure Agent
- Input: Feature specification
- Output: Implementation plan with constitution compliance verification

### 2. Execution Flow
Main Infrastructure Agent → Executor Agent
- Input: Planned task specifications
- Output: Execution status and completion reports

### 3. Review Flow
Executor Agent → Reviewer Agent → Main Infrastructure Agent
- Input: Completed task results
- Output: Validation results and approval/rejection status

### 4. Coordination Flow
Main Infrastructure Agent ↔ All Sub-Agents
- Input: Task assignments and coordination requests
- Output: Status updates and coordination responses

## Protocol Implementation
All communication follows the standardized protocol with authentication, encryption, and error handling as defined in the communication protocol document.