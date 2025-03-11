# Graph state
import operator
from typing import Annotated, TypedDict

from Utils.structured_outputs import Section


class WorkflowState(TypedDict): pass

class JokeGeneratorState(WorkflowState):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str
    
class ParallelWorkflowState(WorkflowState):
    topic: str
    joke: str
    story: str
    poem: str
    combined_output: str
    
class RoutingState(WorkflowState):
    input: str
    decision: str
    output: str
    routing_tries: int

class OrchestratorState(TypedDict):
    topic: str  # Report topic
    sections: list[Section]  # List of report sections
    completed_sections: Annotated[
        list, operator.add
    ]  # All workers write to this key in parallel
    final_report: str  # Final report


class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]

