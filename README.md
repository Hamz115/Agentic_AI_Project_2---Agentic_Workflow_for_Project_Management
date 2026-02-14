# Agentic Workflow for Project Management

**Course:** Agentic Workflows
**Submission:** February 15, 2026

An AI-powered agentic workflow system that transforms product specifications into comprehensive project plans using specialized AI agents.

## Project Overview

This project implements a multi-agent system for automated project management planning. It demonstrates how AI agents can collaborate to analyze product specifications and generate user stories, features, and development tasks.

### Key Features

- **7 Specialized Agents**: DirectPromptAgent, AugmentedPromptAgent, KnowledgeAugmentedPromptAgent, RAGKnowledgePromptAgent, EvaluationAgent, RoutingAgent, ActionPlanningAgent
- **Agentic Workflow**: Orchestrates multiple agents to transform product specs into project plans
- **Evaluation System**: Iterative quality assurance with automatic correction
- **Error Handling**: Robust retry logic and logging for production readiness
- **Flexible Prompts**: Works with different project planning scenarios

## Project Structure

```
.
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── reflection.md            # Project reflection and learnings
├── starter/
│   ├── phase_1/
│   │   ├── workflow_agents/
│   │   │   └── base_agents.py    # All 7 agent implementations
│   │   └── *.py                  # Test scripts for each agent
│   └── phase_2/
│       ├── Product-Spec-Email-Router.txt  # Example product spec
│       └── agentic_workflow.py            # Main workflow script
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Using uv (recommended)
uv venv

# Or using python
python -m venv venv
```

### 2. Activate Virtual Environment

```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
# OR
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example file and add your API key:

```bash
# Copy env.example to .env
copy env.example .env

# Then edit .env and add your actual API key
```

## Running the Project

### Phase 1: Test Individual Agents

```bash
cd starter/phase_1

# Test each agent
python direct_prompt_agent.py
python augmented_prompt_agent.py
python knowledge_augmented_prompt_agent.py
python rag_knowledge_prompt_agent.py
python evaluation_agent.py
python routing_agent.py
python action_planning_agent.py
```

### Phase 2: Run Agentic Workflow

```bash
cd starter/phase_2
python agentic_workflow.py
```

The workflow will:
1. Load the Email Router product specification
2. Extract project planning steps using ActionPlanningAgent
3. Route each step to appropriate teams (Product Manager, Program Manager, Development Engineer)
4. Generate and validate user stories, features, and tasks
5. Save output to `workflow_run_{timestamp}.txt`


## Key Files Explained

| File | Purpose |
|------|---------|
| `base_agents.py` | Contains all 7 agent class implementations |
| `agentic_workflow.py` | Main orchestration script for Phase 2 |
| `Product-Spec-Email-Router.txt` | Example product specification |
| `reflection.md` | Project learnings and improvements |

## Reflection & Learnings

See `reflection.md` for detailed insights including:
- Strengths of the agentic approach
- Error handling improvements
- Limitations and suggested improvements
- Prompt adaptability testing

## Requirements

- Python 3.8+
- openai >= 1.78.1
- pandas >= 2.2.3
- python-dotenv >= 1.1.0

---


