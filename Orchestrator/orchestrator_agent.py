from Utils.nodes import OrchestratorNodes
from Utils.states import OrchestratorState
from IPython.display import Image, display
from config import MODELS
from langgraph.graph import StateGraph, START, END


class OrchestratorWorkflow:
    

    def __init__(self):
        self.graph = StateGraph(OrchestratorState)
        self._initialize_graph_objects()
        self._add_nodes()
        self._add_edges()
        self.workflow = self.graph.compile()
   
    def _initialize_graph_objects(self):
        self.state = OrchestratorState()
        self.nodes = OrchestratorNodes()
        # self.gates = OrchestratorGates()
   
    def _add_nodes(self):
        self.graph.add_node("prompt_user", self.nodes.prompt_user)
        self.graph.add_node("orchestrator", self.nodes.orchestrator)
        self.graph.add_node("llm_call", self.nodes.llm_call)
        self.graph.add_node("synthesizer", self.nodes.synthesizer)
    
    def _add_edges(self):
        self.graph.add_edge(START, "prompt_user")
        self.graph.add_edge("prompt_user", "orchestrator")
        self.graph.add_conditional_edges(
        "orchestrator", self.nodes.assign_workers, ["llm_call"]
    )
        self.graph.add_edge("llm_call", "synthesizer")
        self.graph.add_edge("synthesizer", END)        

    
    def show_workflow(self):
        # Render the graph to a PNG file and display it
        display(Image(self.workflow.get_graph().draw_mermaid_png()))

    
    def run(self) -> OrchestratorState:
        completed_state = self.workflow.invoke({"topic": "None"})
        return completed_state

