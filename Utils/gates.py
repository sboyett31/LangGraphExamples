from Utils.states import WorkflowState


class JokeGeneratorGates:

    def check_punchline(self, state: WorkflowState):
        """Gate function to check if the joke has a punchline"""
        print("Agent> Checking for punchline....")
        # Simple check - does the joke contain "?" or "!"
        if "?" in state["joke"] or "!" in state["joke"]:
            return "Pass"
        return "Fail"

class ParallelWorkflowGates:

    def check_user_input(self, state: WorkflowState):
        """Gate function to check if the user input is valid"""
        print(f"Agent>  Verifying User Input....")
        if state["topic"] not in ["", None, "quit", "exit", "q"]:
            return "Valid"
        return "Invalid"
    
class RoutingGates:
    pass