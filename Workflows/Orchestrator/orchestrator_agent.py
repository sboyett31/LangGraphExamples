# from Nodes.nodes import OrchestratorNodes
# from Utils.states import OrchestratorState
# from IPython.display import Image, display
# from config import MODELS
# from langgraph.graph import StateGraph, START, END
# from Workflows.axovia import AxoviaWorkflow


# class OrchestratorWorkflow(AxoviaWorkflow):
#     def __init__(self):
#         self.graph = StateGraph(OrchestratorState)
#         self._initialize_graph_objects()
#         self._add_nodes()
#         self._add_edges()
#         self.workflow = self.graph.compile()
   
#     def _initialize_graph_objects(self):
#         self.state = OrchestratorState()
#         self.nodes = OrchestratorNodes()
#         # self.Edges = OrchestratorEdges()
   
#     def _add_nodes(self):
#         self.graph.add_node("prompt_user", self.nodes.prompt_user)
#         self.graph.add_node("orchestrator", self.nodes.orchestrator)
#         self.graph.add_node("section_writer", self.nodes.section_writer)
#         self.graph.add_node("synthesizer", self.nodes.synthesizer)
    
#     def _add_edges(self):
#         self.graph.add_edge(START, "prompt_user")
#         self.graph.add_edge("prompt_user", "orchestrator")
#         self.graph.add_conditional_edges(
#         "orchestrator", self.nodes.assign_workers, ["section_writer"]
#     )
#         self.graph.add_edge("section_writer", "synthesizer")
#         self.graph.add_edge("synthesizer", END)        

#     def show_workflow(self):
#         # Render the graph to a PNG file and display it
#         display(Image(self.workflow.get_graph().draw_mermaid_png()))

#     def output_result(self, completed_state: OrchestratorState):
#         # Display the final report
#         print("\nFinal Workflow State:")
#         for k, v in completed_state.items():
#             print(f"{k}: {v}")
    
#     def run(self) -> OrchestratorState:
#         completed_state = self.workflow.invoke({"topic": "None"})
#         self.output_result(completed_state)
#         return completed_state
