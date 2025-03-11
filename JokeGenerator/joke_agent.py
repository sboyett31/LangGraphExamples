from IPython.display import Image, display
from Utils.gates import JokeGeneratorGates
from Utils.nodes import JokeGeneratorNodes
from config import MODELS
from langgraph.graph import StateGraph, START, END
from Utils.states import JokeGeneratorState


class JokeGenerator:
    
    def __init__(self):
        self.graph = StateGraph(JokeGeneratorState)
        self._initialize_graph_objects()
        self._add_nodes()
        self._add_edges()
        self.workflow = self.graph.compile()
   
    def _initialize_graph_objects(self):
        self.state = JokeGeneratorState()
        self.nodes = JokeGeneratorNodes()
        self.gates = JokeGeneratorGates()
   
    def _add_nodes(self):
        self.graph.add_node("prompt_user", self.nodes.prompt_user)
        self.graph.add_node("generate_joke", self.nodes.generate_joke)
        self.graph.add_node("improve_joke", self.nodes.improve_joke)
        self.graph.add_node("polish_joke", self.nodes.polish_joke)
    
    def _add_edges(self):
        self.graph.add_edge(START, "prompt_user")
        self.graph.add_edge("prompt_user", "generate_joke")
        self.graph.add_conditional_edges("generate_joke", self.gates.check_punchline, {"Pass": "improve_joke", "Fail": END})
        self.graph.add_edge("improve_joke", "polish_joke")
        self.graph.add_edge("polish_joke", END)
    
    def show_workflow(self):
        # Render the graph to a PNG file and display it
        display(Image(self.workflow.get_graph().draw_mermaid_png()))

    
    def run(self) -> JokeGeneratorState:
        completed_state = self.workflow.invoke({"topic": "None"})
        return completed_state
