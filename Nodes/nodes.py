# # Nodes
# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# from types import FunctionType
# from typing import List, Literal, TypedDict
# from langchain.schema import SystemMessage, HumanMessage
# from pydantic import BaseModel
# from Nodes.axovia import AxoviaNode
# from Utils.constants import SUPPORTED_NODETYPES
# from Utils.decorators import abstractproperty, debug_node, node, validate_node, validate_type
# from Nodes.prompt_user import ContentPrompt, JokePrompt, Prompt, RequestPrompt, ReportPrompt
# from Utils.states import JokeGeneratorState, OrchestratorState, ParallelWorkflowState, RoutingState, WorkerState, WorkflowState
# from Utils.structured_outputs import JokeResponse, PoemResponse, StoryResponse
# from Utils.types import AxoviaNodeType, NodeDebug
# from config import MODELS
# from langgraph.constants import Send
# from typing import TypeAlias

    
# class ParallelWorkflowNodes:
#     @property
#     def user_prompt(self):
#         return ContentPrompt()

#     def split(self, state: ParallelWorkflowState):
#         """Split the workflow into three parallel LLM calls"""
#         return {"topic": state["topic"]}

#     def create_joke(self, state: ParallelWorkflowState):
#         msg = self.joke_generator(f"Write a joke about {state['topic']}")
#         return {"joke": msg.joke}
    
#     def create_story(self, state: ParallelWorkflowState):
#         msg = self.story_generator(f"Write a story about {state['topic']}")
#         return {"story": msg.story}
    
#     def create_poem(self, state: ParallelWorkflowState):
#         msg = self.poem_generator(f"Write a poem about {state['topic']}")
#         return {"poem": msg.poem}

#     def aggregator(self, state: ParallelWorkflowState):
#         """Combine the joke, story and poem into a single output"""
        
#         combined = f"Here's a story, joke and poem about {state['topic']}!\n\n"
#         combined += f"STORY: {state['story']}\n"
#         combined += f"JOKE: {state['joke']}\n"
#         combined += f"POEM: {state['poem']}"
#         return {"combined_output": combined}


# class RoutingNodes:
#     @property
#     def user_prompt(self):
#         return RequestPrompt()

#     @property
#     def router(self):
#         return self.LLM.router.invoke

#     def clarify_request(self, state: RoutingState):
#         """Clarify the user's request"""
#         response = input(
#             f"{self.PROMPT} '{state['input']}' is ambiguous.\n"
#             "Please clarify if you want a joke, story, or poem: \nUser>  ")
#         return {"input": response}

#     def create_story(self, state: RoutingState):
#         """Write a story"""
#         result = self.story_generator(state["input"])
#         return {"output": result.story}

#     def create_joke(self, state: RoutingState):
#         """Write a joke"""
#         result = self.joke_generator(state["input"])
#         return {"output": result.joke}

#     def create_poem(self, state: RoutingState):
#         """Write a poem"""
#         result = self.poem_generator(state["input"])
#         return {"output": result.poem}

#     def call_router(self, state: RoutingState):
#         """Route the input to the appropriate node"""
#         # Run the augmented LLM with structured output to serve as routing logic
#         decision = self.router(
#             [
#                 SystemMessage(
#                     content="Route the input to story, joke, or poem based on the user's request.  If it is not clear, choose clarify."
#                 ),
#                 HumanMessage(content=state["input"]),
#             ]
#         )
        
#         print(f"DEBUG -> DECISION = {decision}")
#         return {"decision": decision.step}
    
# class OrchestratorNodes():
    
#     @property
#     def user_prompt(self):
#         print("DEBUG -> Executing node: user_prompt (OrchestratorNodes)")
#         return ReportPrompt()

#     def orchestrator(self, state: OrchestratorState):
#         print("DEBUG -> Executing node: orchestrator")
#         """Orchestrator that generates a plan for the report"""
#         # Generate queries
#         report_sections = self.planner(
#             [
#                 SystemMessage(content="Generate a plan for the report."),
#                 HumanMessage(content=f"Here is the report topic: {state['topic']}"),
#             ]
#         )
#         return {"sections": report_sections.sections}

#     def section_writer(self, state: WorkerState):
#         section_name = state['section'].name
#         description = state['section'].description
#         print(f"DEBUG -> Executing node: (section_writer)\n--------\n     section_name: {section_name}\n     description: {description}\n--------\n")
#         """Worker writes a section of the report"""
        
#         # Generate section
#         section = self.LLM.sonnet.invoke(
#             [
#                 SystemMessage(
#                     content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."
#                 ),
#                 HumanMessage(
#                     content=f"Here is the section name: {state['section'].name} and description: {state['section'].description}"
#                 ),
#             ]
#         )
#         # Write the updated section to completed sections
#         return {"completed_sections": [section.content]}

#     def synthesizer(self, state: OrchestratorState):
#         print("DEBUG -> Executing node: synthesizer")
#         """Synthesize full report from sections"""
#         # List of completed sections
#         completed_sections = state["completed_sections"]
        
#         print(f"DEBUG -> completed_sections: {completed_sections}")
#         # Format completed section to str to use as context for final sections
#         completed_report_sections = "\n\n---\n\n".join(completed_sections)
#         print(f"DEBUG -> final_report: {completed_report_sections}")
        
#         return {"final_report": completed_report_sections}

#     def assign_workers(self, state: OrchestratorState):
#         print("DEBUG -> Executing node: assign_workers")
#         """Assign a worker to each section in the plan"""
#         # Kick off section writing in parallel via Send() API
#         return [Send("section_writer", {"section": s}) for s in state["sections"]]
