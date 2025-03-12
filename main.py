import sys
import os
from typing import List, Dict, Any

from Workflows.JokeGenerator.joke_gen import JokeGenerator
# from Workflows.Orchestrator.orchestrator_agent import OrchestratorWorkflow
# from Workflows.ParallelChains.parallel_agents import ParallelGenerator
# from Workflows.Routing.routing_agent import RoutingWorkflow

# Add current directory to sys.path to resolve local module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import dotenv

# Import agent implementations


def run_workflow(workflow):
    """Run the workflow agent."""
    print(f" running workflow: {workflow.__class__.__name__}")
    # Create and run the workflow
    end_state = workflow.run()
    
    # Display the workflow
    print("\nWorkflow:")
    # workflow.show_workflow()
    
    # Check workflow type and display appropriate outputs
    if workflow.__class__.__name__ == "JokeGenerator":
        print("\nGenerated Joke:")
        print(end_state.get('final_joke'))
        print("\nJoke Generation Process:")
        print(f"Initial Joke: {end_state.get('joke')}")
        print(f"Improved Joke: {end_state.get('improved_joke')}")
        print(f"Final Polished Joke: {end_state.get('final_joke')}")
    # elif workflow.__class__.__name__ == "ParallelGenerator":
    #     print("\nGenerated Content:")
    #     print(end_state.get('combined_output'))
    #     print("\nIndividual Components:")
    #     print(f"Joke: {end_state.get('joke')}")
    #     print(f"Story: {end_state.get('story')}")
    #     print(f"Poem: {end_state.get('poem')}")
    # elif workflow.__class__.__name__ == "RoutingWorkflow":
    #     print("\nGenerated Content:")
    #     print(end_state.get('output'))
    #     print("\nRouting Information:")
    #     print(f"User Input: {end_state.get('input')}")
    #     print(f"Routing Decision: {end_state.get('decision')}")
    # elif workflow.__class__.__name__ == "OrchestratorWorkflow":
    #     print("\nGenerated Content:")
    #     print(end_state.get('final_report'))
    #     print("\nRouting Information:")
    #     print(f"Topic: {end_state.get('topic')}")


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
        # {
        #     "name": "Parallel Generator",
        #     "description": "Generate joke, story, and poem on a given topic using a graph-based workflow",
        #     "workflow": ParallelGenerator() 
        # },
        # {
        #     "name": "Content Router",
        #     "description": "Intelligently route your request to generate a joke, story, or poem",
        #     "workflow": RoutingWorkflow()
        # },
        # {
        #     "name": "Report Generator",
        #     "description": "Intelligently create a report about a topic of your choosing",
        #     "workflow": OrchestratorWorkflow()
        # },
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