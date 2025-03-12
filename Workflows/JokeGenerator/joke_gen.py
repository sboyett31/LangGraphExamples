from dataclasses import dataclass
from types import FunctionType
from typing import TypedDict, Dict, Any, Callable
from IPython.display import Image, display
from Nodes.generators import FinalizeJoke, GenerateJoke, ImproveJoke
from Nodes.prompt_user import JokePrompt
from Utils.analyzers import check_punchline

from langgraph.graph import StateGraph, START, END
from Utils.states import JokeGeneratorState, WorkflowState

class AxoviaEdge(TypedDict):
    source: str
    target: str
    
class AxoviaConditionalEdge(TypedDict):
    source: str
    gate: FunctionType
    output_map: dict


class AxoviaWorkflow:
    STATE = None
    NODES, EDGES, CONDITIONAL_EDGES = [], [], []
    
    def __init__(self):
        self.graph = StateGraph(self.STATE)
        self.compile()
    
    def compile(self):
        self._add_nodes()
        self._add_edges()
        self.workflow = self.graph.compile()
        
    def _add_nodes(self):
        """Add all nodes to the graph"""
        node_instances = {}
        
        for node_class in self.NODES:
            # Create a node instance
            node_instance = node_class()
            node_name = node_instance.name
            node_instances[node_name] = node_instance
            
            # Use a proper closure to bind the instance
            def create_node_func(instance=node_instance):
                return lambda state: instance.method(state)
            
            # Add to graph with bound method
            self.graph.add_node(node_name, create_node_func())

    def _add_edges(self):
        """Add all edges to the graph"""
        for edge_tuple in self.EDGES:
            self.graph.add_edge(edge_tuple[0], edge_tuple[1])
            
        for edge_tuple in self.CONDITIONAL_EDGES:
            self.graph.add_conditional_edges(
                edge_tuple[0],  # source
                edge_tuple[2],  # gate function
                edge_tuple[3]   # path map
            )
            
    def show_workflow(self):
        # Render the graph to a PNG file and display it
        display(Image(self.workflow.get_graph().draw_mermaid_png()))
        
    def run(self) -> WorkflowState:
        completed_state = self.workflow.invoke({"topic": "None"})
        return completed_state


class JokeGenerator(AxoviaWorkflow):
    
    STATE = JokeGeneratorState
    
    # Node classes
    NODES = [JokePrompt, GenerateJoke, ImproveJoke, FinalizeJoke]
    
    # Regular edges as (source, target) tuples
    EDGES = [
        (START, "prompt_user"),
        ("prompt_user", "generate_joke"),
        ("improve_joke", "finalize_joke"),
        ("finalize_joke", END)
    ]
    
    CONDITIONAL_EDGES = [
        ("generate_joke", "improve_joke", check_punchline, {"Pass": "improve_joke", "Fail": END})
    ]

