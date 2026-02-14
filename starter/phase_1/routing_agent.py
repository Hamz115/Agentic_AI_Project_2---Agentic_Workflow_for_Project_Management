
# TODO: 1 - Import the KnowledgeAugmentedPromptAgent and RoutingAgent
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, RoutingAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

persona = "You are a college professor"

knowledge = "You know everything about Texas"
# TODO: 2 - Define the Texas Knowledge Augmented Prompt Agent
texas_agent = KnowledgeAugmentedPromptAgent(openai_api_key, "You are a Texas expert", "You know everything about Texas")

knowledge = "You know everything about Europe"
# TODO: 3 - Define the Europe Knowledge Augmented Prompt Agent
europe_agent = KnowledgeAugmentedPromptAgent(openai_api_key, "You are a Europe expert", "You know everything about Europe")

persona = "You are a college math professor"
knowledge = "You know everything about math, you take prompts with numbers, extract math formulas, and show the answer without explanation"
# TODO: 4 - Define the Math Knowledge Augmented Prompt Agent
math_agent = KnowledgeAugmentedPromptAgent(openai_api_key, "You are a math professor", "You know everything about math")

routing_agent = RoutingAgent(openai_api_key, [])
agents = [
    {
        "name": "Texas Agent",
        "description": "Answer a question about Texas",
        # TODO: 5 - Call the Texas Agent to respond to prompts
        "func": lambda x: texas_agent.respond(x)
    },
    {
        "name": "Europe Agent",
        "description": "Answer a question about Europe",
        # TODO: 6 - Define a function to call the Europe Agent
        "func": lambda x: europe_agent.respond(x)
    },
    {
        "name": "Math Agent",
        "description": "When a prompt contains numbers, respond with a math formula",
        # TODO: 7 - Define a function to call the Math Agent
        "func": lambda x: math_agent.respond(x)
    }
]

routing_agent.agents = agents

# TODO: 8 - Print the RoutingAgent responses to the following prompts:
#           - "Tell me about the history of Rome, Texas"
#           - "Tell me about the history of Rome, Italy"
#           - "One story takes 2 days, and there are 20 stories"

print("Prompt 1: Tell me about the history of Rome, Texas")
result1 = routing_agent.route("Tell me about the history of Rome, Texas")
print(result1)
print()

print("Prompt 2: Tell me about the history of Rome, Italy")
result2 = routing_agent.route("Tell me about the history of Rome, Italy")
print(result2)
print()

print("Prompt 3: One story takes 2 days, and there are 20 stories")
result3 = routing_agent.route("One story takes 2 days, and there are 20 stories")
print(result3)
