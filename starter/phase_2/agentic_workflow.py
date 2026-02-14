# agentic_workflow.py

import sys
import os
import logging
import time
from datetime import datetime

# Add parent directory to path to import workflow_agents from phase_1
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'phase_1'))

# Setup output file (for terminal-like output)
output_filename = f"workflow_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
output_file = open(output_filename, 'w', encoding='utf-8')

# Custom print to save to file
original_print = print
def print(*args, **kwargs):
    original_print(*args, **kwargs)
    original_print(*args, file=output_file, **kwargs)
    output_file.flush()

# Setup logging
log_filename = f"workflow_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import agents
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    logger.error("OPENAI_API_KEY not found in environment variables")
    output_file.close()
    raise ValueError("OPENAI_API_KEY not found. Please check .env file.")

# Load product spec
product_spec_path = os.path.join(os.path.dirname(__file__), '..', 'phase_2', 'Product-Spec-Email-Router.txt')
try:
    with open(product_spec_path, "r") as f:
        product_spec = f.read()
    logger.info(f"Successfully loaded product spec ({len(product_spec)} characters)")
except FileNotFoundError:
    logger.error(f"Product spec file not found: {product_spec_path}")
    output_file.close()
    raise
except Exception as e:
    logger.error(f"Error loading product spec: {e}")
    output_file.close()
    raise

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
    + product_spec
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_product_manager, knowledge_product_manager)

# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_product_manager = (
    "The answer should be user stories that follow the following structure: "
    "As a [type of user], I want [an action or feature] so that [benefit/value]. "
    "Each story should have a clear persona, action, and benefit."
)
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_product_manager_eval,
    evaluation_criteria_product_manager,
    product_manager_knowledge_agent,
    max_interactions=3
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_program_manager, knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
evaluation_criteria_program_manager = (
    "The answer should be product features that follow the following structure: "
    "Feature Name: A clear, concise title that identifies the capability\n"
    "Description: A brief explanation of what the feature does and its purpose\n"
    "Key Functionality: The specific capabilities or actions the feature provides\n"
    "User Benefit: How this feature creates value for the user"
)
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_program_manager_eval,
    evaluation_criteria_program_manager,
    program_manager_knowledge_agent,
    max_interactions=3
)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
evaluation_criteria_dev_engineer = (
    "The answer should be tasks following this exact structure: "
    "Task ID: A unique identifier for tracking purposes\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first"
)
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_dev_engineer_eval,
    evaluation_criteria_dev_engineer,
    development_engineer_knowledge_agent,
    max_interactions=3
)


# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.

def product_manager_support_function(query):
    """Product Manager team: generates and validates user stories"""
    print(f"\n[Product Manager Team] Processing: {query}")
    # Get response from knowledge agent
    response = product_manager_knowledge_agent.respond(query)
    print(f"[Product Manager] Raw response:\n{response}")
    # Evaluate the response
    evaluation_result = product_manager_evaluation_agent.evaluate(query)
    print(f"[Product Manager] Evaluation result: {evaluation_result['evaluation']}")
    return evaluation_result['final_response']

def program_manager_support_function(query):
    """Program Manager team: generates and validates features"""
    print(f"\n[Program Manager Team] Processing: {query}")
    # Get response from knowledge agent
    response = program_manager_knowledge_agent.respond(query)
    print(f"[Program Manager] Raw response:\n{response}")
    # Evaluate the response
    evaluation_result = program_manager_evaluation_agent.evaluate(query)
    print(f"[Program Manager] Evaluation result: {evaluation_result['evaluation']}")
    return evaluation_result['final_response']

def development_engineer_support_function(query):
    """Development Engineer team: generates and validates tasks"""
    print(f"\n[Development Engineer Team] Processing: {query}")
    # Get response from knowledge agent
    response = development_engineer_knowledge_agent.respond(query)
    print(f"[Development Engineer] Raw response:\n{response}")
    # Evaluate the response
    evaluation_result = development_engineer_evaluation_agent.evaluate(query)
    print(f"[Development Engineer] Evaluation result: {evaluation_result['evaluation']}")
    return evaluation_result['final_response']

# Define routes for RoutingAgent
routes = [
    {
        "name": "Product Manager",
        "description": "Creating user stories from product requirements",
        "func": product_manager_support_function
    },
    {
        "name": "Program Manager",
        "description": "Defining features and organizing user stories",
        "func": program_manager_support_function
    },
    {
        "name": "Development Engineer",
        "description": "Creating development tasks and engineering work",
        "func": development_engineer_support_function
    }
]

# Instantiate RoutingAgent
routing_agent = RoutingAgent(openai_api_key, routes)

# Run the workflow

print("\n*** Workflow execution started ***\n")

try:
    # Workflow Prompt
    workflow_prompt = "Generate a risk assessment plan for the Email Router based on its specification"
    print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

    print("\nDefining workflow steps from the workflow prompt")

    # Extract steps from workflow prompt
    try:
        workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
        logger.info(f"Extracted {len(workflow_steps)} workflow steps")
        print(f"Extracted workflow steps: {workflow_steps}")
    except Exception as e:
        logger.error(f"Failed to extract workflow steps: {e}")
        print(f"ERROR: Failed to extract workflow steps: {e}")
        workflow_steps = []

    # Initialize completed steps list
    completed_steps = []

    # Process each step
    for i, step in enumerate(workflow_steps):
        print(f"\n--- Processing step {i+1}/{len(workflow_steps)}: {step} ---")
        logger.info(f"Processing step: {step}")
        try:
            result = routing_agent.route(step)
            completed_steps.append({
                "step": step,
                "result": result
            })
            print(f"Step completed: {step}")
            print(f"Result:\n{result}\n")
        except Exception as e:
            logger.error(f"Failed to process step '{step}': {e}")
            print(f"ERROR: Failed to process step: {e}")
            completed_steps.append({
                "step": step,
                "result": f"ERROR: Failed to process - {str(e)}"
            })
            continue

    # Print final output
    print("\n*** Workflow execution completed ***")
    print("Final project plan:")
    print("=" * 50)
    for item in completed_steps:
        print(f"\n{item['step']}:")
        print("-" * 30)
        print(item['result'])

    logger.info(f"Workflow completed successfully with {len(completed_steps)} steps")

except Exception as e:
    logger.error(f"Workflow failed with error: {e}")
    print(f"\n!!! WORKFLOW FAILED: {e} !!!")
    print("Check the log file for details.")

finally:
    # Close the output file
    print(f"\nOutput saved to: {output_filename}")
    output_file.close()
