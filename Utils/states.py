# Graph state
from typing import TypedDict


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
