import sys
from typing import List, Dict, Any, Callable

import dotenv

# Import agent implementations
from JokeGenerator.joke_agent import JokeGenerator
from Orchestrator.orchestrator_agent import OrchestratorWorkflow
from ParallelChains.parallel_agents import ParallelGenerator
from Routing.routing_agent import RoutingWorkflow
from Utils.structured_outputs import SearchQuery
from Utils.tools import multiply
from config import MODELS


def run_workflow(workflow):
    """Run the workflow agent."""
    print(f" running workflow: {workflow.__class__.__name__}")
    # Create and run the workflow
    result = workflow.run()
    
    # Display the workflow
    print("\nWorkflow:")
    # workflow.show_workflow()
    
    # Check workflow type and display appropriate outputs
    if workflow.__class__.__name__ == "JokeGenerator":
        print("\nGenerated Joke:")
        print(result.get('final_joke'))
        print("\nJoke Generation Process:")
        print(f"Initial Joke: {result.get('joke')}")
        print(f"Improved Joke: {result.get('improved_joke')}")
        print(f"Final Polished Joke: {result.get('final_joke')}")
    elif workflow.__class__.__name__ == "ParallelGenerator":
        print("\nGenerated Content:")
        print(result.get('combined_output'))
        print("\nIndividual Components:")
        print(f"Joke: {result.get('joke')}")
        print(f"Story: {result.get('story')}")
        print(f"Poem: {result.get('poem')}")
    elif workflow.__class__.__name__ == "RoutingWorkflow":
        print("\nGenerated Content:")
        print(result.get('output'))
        print("\nRouting Information:")
        print(f"User Input: {result.get('input')}")
        print(f"Routing Decision: {result.get('decision')}")
    elif workflow.__class__.__name__ == "OrchestratorWorkflow":
        print("\nGenerated Content:")
        print(result.get('output'))
        print("\nRouting Information:")
        print(f"User Input: {result.get('input')}")



def display_menu(options: List[Dict[str, Any]]):
    """Display a menu of options and return the user's choice."""
    print("\n" + "=" * 50)
    print("LangGraph Agent CLI")
    print("=" * 50)
    print("Select a graph agent to run:")
    
    for i, option in enumerate(options, 1):
        print(f"{i}. {option['name']} - {option['description']}")
    
    print(f"{len(options) + 1}. Exit")
    print("-" * 50)
    
    while True:
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(options) + 1 or choice in ['exit', 'quit', 'q']:
                return choice
            else:
                print(f"Please enter a number between 1 and {len(options) + 1}")
        except ValueError:
            print("Please enter a valid number")


def main():
    """Main CLI function to run different graph agents."""
    # Define available agents
    dotenv.load_dotenv()
    agents = [
        {
            "name": "Joke Generator",
            "description": "Generate jokes on a given topic using a graph-based workflow",
            "workflow": JokeGenerator()
        },
        {
            "name": "Parallel Generator",
            "description": "Generate joke, story, and poem on a given topic using a graph-based workflow",
            "workflow": ParallelGenerator() 
        },
        {
            "name": "Content Router",
            "description": "Intelligently route your request to generate a joke, story, or poem",
            "workflow": RoutingWorkflow()
        },
        {
            "name": "Report Generator",
            "description": "Intelligently create a report about a topic of your choosing",
            "workflow": OrchestratorWorkflow()
        },
    ]
    
    while True:
        choice = display_menu(agents)
                
        # Check if user wants to exit
        if choice == len(agents) + 1 or choice in ['exit', 'quit', 'q']:
            print("\nExiting. Goodbye!")
            sys.exit(0)
        
        # Run the selected agent
        selected_agent = agents[choice - 1]
        try:
            run_workflow(selected_agent["workflow"])
            
            # Ask if user wants to run another agent
            again = input("\nWould you like to run another agent? (y/n): ").lower()
            if again != 'y':
                print("\nExiting. Goodbye!")
                break
                
        except Exception as e:
            print(f"\nError running {selected_agent['name']}: {str(e)}")


if __name__ == "__main__":
    main()