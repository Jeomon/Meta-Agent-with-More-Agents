# Meta Agent with More Agents: AI Task Delegation Workflow

## Description

**Meta Agent with More Agents** is a project designed to dynamically delegate complex queries to specialized AI agents. At the core of the system is the **Meta Agent**, which orchestrates the problem-solving process by breaking down queries into sub-tasks and assigning each to the most suitable agent. These agents either solve sub-tasks using tools (via the **ReAct Agent**) or by reasoning step-by-step (via the **Chain of Thought Agent**). The Meta Agent continues this iterative process until the entire task is solved, providing the final answer to the user.

## Architecture Overview

![Image of the Workflow](diagram.svg)

## Demo

[Project Demo Videos](https://drive.google.com/drive/folders/1VIYrazLOvcANW7OSCSGWBGZmZ-zz4NZV?usp=sharing)

Note: Sometimes it will fail and demo might seem stuck at some time. It's actually because I limited the rate of API calls to prevent hitting the rate limit.

The project employs a hierarchical and flexible design:

- **Meta Agent:** Manages the overall query-solving process by determining how to break down tasks and assigning them to appropriate agents based on the task's requirements. The user can now provide their own agents, which the Meta Agent will consider when assigning tasks.
- **User-Created Agents:** Users can create and assign their own agents to tasks. If the Meta Agent determines that a user-provided agent is suitable, it will utilize that agent. If not, the Meta Agent will create its own agent.
- **ReAct Agent:** Handles tasks that require external tools. It either executes the query with existing tools or, when needed, requests tool creation, updates, or deletions via the **Tool Agent**.
- **Tool Agent:** Dynamically creates, updates, or deletes tools required by the ReAct Agent to handle specific tasks. It can remove a tool if it fails to work correctly, doesn't produce the intended output even after debugging, or if the user requests its removal.
- **Chain of Thought (CoT) Agent:** Processes tasks that do not require external tools, solving them through an iterative reasoning approach.

This architecture ensures smooth communication between agents and enables dynamic tool creation, updating, or deletion to expand the problem-solving capabilities.

### Workflow

1. The **Meta Agent** receives a query.
2. It analyzes the task and determines whether it requires tools or iterative reasoning:
   - If tools are needed, the **ReAct Agent** is invoked.
   - If no tools are required, the **CoT Agent** is engaged.
3. The user can provide their own agents for the Meta Agent to consider. If the Meta Agent finds the user-provided agent suitable, it will assign the task to it.
4. If the **ReAct Agent** determines that a required tool is missing or not functioning, it invokes the **Tool Agent** to create, update, or delete the tool.
5. Sub-tasks are solved incrementally, with results passed back to the **Meta Agent**.
6. The process continues until the entire query is resolved.

## Key Features

- **Dynamic Task Delegation:** Automatically assigns sub-tasks to specialized agents based on task type and complexity.
- **User-Created Agents:** Users can provide their own agents, which the Meta Agent can utilize if deemed appropriate.
- **Tool Creation, Updates, & Deletion:** The **Tool Agent** can dynamically generate, update, or delete tools at runtime based on task requirements or failures.
- **Iterative Reasoning (Chain of Thought):** Solves tasks without tools by breaking them down into smaller reasoning steps.
- **Hierarchical Problem Solving:** Complex queries are divided into smaller, manageable sub-tasks that are solved iteratively.
- **Modular Design:** Agents can be easily expanded or replaced, allowing for flexibility and scalability.
- **User-Controlled Tool Access:** Users have the power to grant tool access to the agents, enabling customized functionality based on specific task needs.

## Tool Deletion Feature

In addition to creating and updating tools, the **Tool Agent** has the ability to delete tools when necessary. The **ReAct Agent** can request the **Tool Agent** to remove a tool under the following circumstances:
- The tool is failing or not producing the desired output.
- Debugging efforts are unsuccessful.
- The user requests to remove the tool.

This ensures that non-functional tools do not hinder the system's performance, and the workflow remains efficient.

## Installation

To set up the project, ensure you have Python 3.x installed, then run the following command to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

To run the ReAct Agent with Tool Agent, execute the following command:

```bash
python app.py
```

## Usage

To start using **Meta Agent with More Agents**, follow these steps:

1. Provide a query to the **Meta Agent**.
2. The **Meta Agent** will create a system prompt and assign the task to either the **ReAct Agent** (if tools are required) or the **CoT Agent** (if the task relies on reasoning).
3. Users can provide their own agents, and if the Meta Agent finds a user-provided agent suitable, it will utilize it. If not, the Meta Agent will create its own agent.
4. If tools are missing, outdated, or non-functional, the **Tool Agent** will dynamically create, update, or remove them.
5. Sub-tasks are solved iteratively, with results compiled and provided as a final answer to the user.

### Example Queries

<examples>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- **Meta Agent:** [Meta Prompting](https://www.promptingguide.ai/techniques/meta-prompting)
- **React Agent:** [ReAct Prompting](https://www.promptingguide.ai/techniques/react)
- **CoT Agent:** [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot)
- **Reflexion in CoT Agent:** [Reflexion](https://www.promptingguide.ai/techniques/reflexion)

## Contact

If you have any questions, suggestions, or feedback, feel free to contact us:

- **Email**: jeogeoalukka@gmail.com