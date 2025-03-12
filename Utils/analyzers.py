from Utils.states import WorkflowState # RoutingState,

def check_punchline(state: WorkflowState):
    """Gate function to check if the joke has a punchline"""
    print("Agent> Checking for punchline....")
    # Simple check - does the joke contain "?" or "!"
    if "?" in state["joke"] or "!" in state["joke"]:
        return "Pass"
    return "Fail"

# class ParallelWorkflowEdges:

#     def check_user_input(self, state: WorkflowState):
#         """Gate function to check if the user input is valid"""
#         print(f"Agent>  Verifying User Input....")
#         if state["topic"] not in ["", None, "quit", "exit", "q"]:
#             return "Valid"
#         return "Invalid"
    
# class RoutingEdges:
    
#     def route_decision(self, state: RoutingState):
#         if state.get("routing_tries") is None:
#             state["routing_tries"] = 0
#         print(f"routing decision... routing tries = {state.get('routing_tries')}")
#         state["routing_tries"] = state.get("routing_tries") + 1
#         if state["routing_tries"] > 3:
#             return "end"
#         if state.get("decision") in ["story", "joke", "poem"]:
#             print(f"DEBUG -> routing to {state.get('decision')}")
#             return state.get("decision")
#         else:
#             print(f"DEBUG -> Invalid decision")
#             return "invalid_decision"

