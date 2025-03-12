# Graph state
import operator
from typing import Annotated, List, Literal, TypedDict

# from Utils.structured_outputs import Section
from typing import List, Literal

class WorkflowError(TypedDict):
    type: Literal["Warning", "Error"]
    message: str

class WorkflowState(TypedDict, total=False): 
    complete: bool = False
    errors: List[WorkflowError] = [] # Any errors that happen during workflow execution

class JokeGeneratorState(WorkflowState):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str
    
# class ParallelWorkflowState(WorkflowState):
#     topic: str
#     joke: str
#     story: str
#     poem: str
#     combined_output: str

# # Other states remain similar, for example:
# class RoutingState(WorkflowState):
#     input: str
#     decision: str
#     output: str
#     routing_tries: int  # Max value of 10 for routing_tries (expected to be <= 10)

# class OrchestratorState(WorkflowState):
#     topic: str  # Report topic
#     sections: list[Section]  # List of report sections
#     completed_sections: Annotated[
#         list, operator.add
#     ]  # All workers write to this key in parallel
#     final_report: str  # Final report


# class WorkerState(WorkflowState):
#     section: Section
#     completed_sections: Annotated[list, operator.add]

