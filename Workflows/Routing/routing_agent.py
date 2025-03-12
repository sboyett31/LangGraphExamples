# from IPython.display import Image, display
# from Utils.edges import RoutingEdges
# from Nodes.nodes import  RoutingNodes
# from langgraph.graph import StateGraph, START, END
# from Utils.states import RoutingState


# class RoutingWorkflow:
       
#     ROUTES = {
#         "story": "create_story",
#         "joke": "create_joke",
#         "poem": "create_poem",
#         "invalid_decision": "clarify_request",
#         "end": END
#     }

#     def __init__(self):
#         self.graph = StateGraph(RoutingState)
#         self._initialize_graph_objects()
#         self._add_nodes()
#         self._add_edges()
#         self.workflow = self.graph.compile()
   
#     def _initialize_graph_objects(self):
#         self.state = RoutingState()
#         self.nodes = RoutingNodes()
#         self.Edges = RoutingEdges()
   
#     def _add_nodes(self):
#         self.graph.add_node("prompt_user", self.nodes.prompt_user)
#         self.graph.add_node("create_joke", self.nodes.create_joke)
#         self.graph.add_node("create_story", self.nodes.create_story)
#         self.graph.add_node("create_poem", self.nodes.create_poem)
#         self.graph.add_node("call_router", self.nodes.call_router)
#         self.graph.add_node("clarify_request", self.nodes.clarify_request)
        
    
#     def _add_edges(self):
#         self.graph.add_edge(START, "prompt_user")
#         self.graph.add_edge("prompt_user", "call_router")
#         self.graph.add_conditional_edges(
#             source="call_router", 
#             path=self.Edges.route_decision,
#             path_map=self.ROUTES
#         )
#         self.graph.add_edge("create_joke", END)
#         self.graph.add_edge("create_story", END)
#         self.graph.add_edge("create_poem", END)
#         self.graph.add_edge("clarify_request", "call_router")
        
#     def show_workflow(self):
#         # Render the graph to a PNG file and display it
#         display(Image(self.workflow.get_graph().draw_mermaid_png()))
        
#     def run(self):
#         # Get user input
#         state = self.workflow.invoke({"input": "", "decision": "", "output": ""})
#         return state
