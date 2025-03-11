from IPython.display import Image, display
from Utils.gates import ParallelWorkflowGates
from Utils.nodes import ParallelWorkflowNodes
from langgraph.graph import StateGraph, START, END
from Utils.states import ParallelWorkflowState


class ParallelGenerator:
    
    def __init__(self):
        self.graph = StateGraph(ParallelWorkflowState)
        self._initialize_graph_objects()
        self._add_nodes()
        self._add_edges()
        self.workflow = self.graph.compile()
   
    def _initialize_graph_objects(self):
        self.state = ParallelWorkflowState()
        self.nodes = ParallelWorkflowNodes()
        self.gates = ParallelWorkflowGates()
   
    def _add_nodes(self):
        self.graph.add_node("prompt_user", self.nodes.prompt_user)
        self.graph.add_node("split", self.nodes.split)
        self.graph.add_node("create_joke", self.nodes.create_joke)
        self.graph.add_node("create_story", self.nodes.create_story)
        self.graph.add_node("create_poem", self.nodes.create_poem)
        self.graph.add_node("aggregator", self.nodes.aggregator)    
    
    def _add_edges(self):
        self.graph.add_edge(START, "prompt_user")
        self.graph.add_conditional_edges("prompt_user", self.gates.check_user_input, {"Valid": "split", "Invalid": END})      
        self.graph.add_edge("split", "create_joke")
        self.graph.add_edge("split", "create_story")
        self.graph.add_edge("split", "create_poem")
        self.graph.add_edge("create_joke", "aggregator")
        self.graph.add_edge("create_story", "aggregator")
        self.graph.add_edge("create_poem", "aggregator")
        
    def show_workflow(self):
        # Render the graph to a PNG file and display it
        display(Image(self.workflow.get_graph().draw_mermaid_png()))

        
    def run(self) -> ParallelWorkflowState:
        print(f"invoking")
        completed_state = self.workflow.invoke({"topic": "None"})
        print(f"finished invoking")
        return completed_state
