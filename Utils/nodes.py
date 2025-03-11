# Nodes
from abc import ABC, abstractmethod
from dataclasses import dataclass
from langchain.schema import SystemMessage, HumanMessage
from Utils.states import JokeGeneratorState, OrchestratorState, ParallelWorkflowState, RoutingState, WorkerState
from Utils.structured_outputs import JokeResponse, PoemResponse, StoryResponse
from config import MODELS
from langgraph.constants import Send

@dataclass
class Prompt:
    text: str
    var: str

@dataclass
class JokePrompt(Prompt):
    text: str = "Enter a topic for your joke: "
    var: str = "topic"
    
@dataclass
class ReportPrompt(Prompt):
    text: str = "Enter a topic for your report: "
    var: str = "topic"

@dataclass
class ContentPrompt(Prompt):
    text: str = "Enter a topic for your content: "
    var: str = "topic"
    
@dataclass
class RequestPrompt(Prompt):
    text: str = "Enter A request for the Agent: "
    var: str = "input"

class ClaudeNodes(ABC):
    LLM: str = MODELS.Anthropic.Claude_3_5
    PROMPT: str = "Axovia>  "
        
    @property
    @abstractmethod
    def user_prompt(self) -> Prompt:
        print("DEBUG -> Executing node: user_prompt (property)")
        raise NotImplementedError("User prompt not implemented")
    
    @property
    def joke_generator(self):
        print("DEBUG -> Executing node: joke_generator (property)")
        return self.LLM.joke_gen.invoke

    @property
    def story_generator(self):
        print("DEBUG -> Executing node: story_generator (property)")
        return self.LLM.story_gen.invoke

    @property
    def poem_generator(self):
        print("DEBUG -> Executing node: poem_generator (property)")
        return self.LLM.poem_gen.invoke
    
    @property
    def planner(self):
        print("DEBUG -> Executing node: planner (property)")
        return self.LLM.planner.invoke

    def output(self, msg: str):
        print("DEBUG -> Executing node: output")
        print(f"{self.PROMPT} {msg}")

    def prompt_user(self, state: JokeGeneratorState) -> str:
        print("DEBUG -> Executing node: prompt_user")
        response = input(f"{self.PROMPT} {self.user_prompt.text}: ")
        return {self.user_prompt.var: response}


# Nodes
class JokeGeneratorNodes(ClaudeNodes):
    
    @property
    def user_prompt(self):
        print("DEBUG -> Executing node: user_prompt (JokeGeneratorNodes)")
        return JokePrompt()
    
    def generate_joke(self, state: JokeGeneratorState) -> str:
        print("DEBUG -> Executing node: generate_joke")
        self.output("Generating joke....")
        msg = self.joke_generator(f"Write a short joke about {state['topic']}")
        print(f"generated joke output: {msg}")
        return {"joke": msg.joke}
    
    def improve_joke(self, state: JokeGeneratorState) -> str:
        print("DEBUG -> Executing node: improve_joke")
        self.output("Improving joke....")
        msg = self.joke_generator(f"Make this joke funnier by adding wordplay: {state['joke']}")
        return {"improved_joke": msg.joke}
    
    def polish_joke(self, state: JokeGeneratorState) -> str:
        print("DEBUG -> Executing node: polish_joke")
        self.output("Polishing joke....")
        msg = self.joke_generator(f"Add a surprising twist to this joke: {state['improved_joke']}")
        return {"final_joke": msg.joke}


class ParallelWorkflowNodes(ClaudeNodes):
    
    @property
    def user_prompt(self):
        print("DEBUG -> Executing node: user_prompt (ParallelWorkflowNodes)")
        return ContentPrompt()

    def split(self, state: ParallelWorkflowState):
        print("DEBUG -> Executing node: split")
        """Split the workflow into three parallel LLM calls"""
        return {"topic": state["topic"]}

    def create_joke(self, state: ParallelWorkflowState):
        print("DEBUG -> Executing node: create_joke")
        print("DEBUG -> joke")
        msg = self.joke_generator(f"Write a joke about {state['topic']}")
        return {"joke": msg.joke}
    
    def create_story(self, state: ParallelWorkflowState):
        print("DEBUG -> Executing node: create_story")
        print("DEBUG -> story")
        msg = self.story_generator(f"Write a story about {state['topic']}")
        return {"story": msg.story}
    
    def create_poem(self, state: ParallelWorkflowState):
        print("DEBUG -> Executing node: create_poem")
        print("DEBUG -> poem")
        msg = self.poem_generator(f"Write a poem about {state['topic']}")
        return {"poem": msg.poem}

    def aggregator(self, state: ParallelWorkflowState):
        print("DEBUG -> Executing node: aggregator")
        """Combine the joke, story and poem into a single output"""
        
        combined = f"Here's a story, joke and poem about {state['topic']}!\n\n"
        combined += f"STORY: {state['story']}\n"
        combined += f"JOKE: {state['joke']}\n"
        combined += f"POEM: {state['poem']}"
        return {"combined_output": combined}


class RoutingNodes(ClaudeNodes):

    @property
    def user_prompt(self):
        print("DEBUG -> Executing node: user_prompt (RoutingNodes)")
        return RequestPrompt()

    @property
    def router(self):
        print("DEBUG -> Executing node: router (property)")
        return self.LLM.router.invoke

    def clarify_request(self, state: RoutingState):
        print("DEBUG -> Executing node: clarify_request")
        """Clarify the user's request"""
        prev_input = state["input"]
        response = input(
            f"{self.PROMPT} '{state['input']}' is ambiguous.\n"
            "Please clarify if you want a joke, story, or poem: \nUser>  ")
        return {"input": response}

    def create_story(self, state: RoutingState):
        print("DEBUG -> Executing node: create_story")
        """Write a story"""
        result = self.story_generator(state["input"])
        return {"output": result.story}

    def create_joke(self, state: RoutingState):
        print("DEBUG -> Executing node: create_joke")
        """Write a joke"""
        result = self.joke_generator(state["input"])
        return {"output": result.joke}

    def create_poem(self, state: RoutingState):
        print("DEBUG -> Executing node: create_poem")
        """Write a poem"""
        result = self.poem_generator(state["input"])
        return {"output": result.poem}

    def call_router(self, state: RoutingState):
        print("DEBUG -> Executing node: call_router")
        """Route the input to the appropriate node"""
        # Run the augmented LLM with structured output to serve as routing logic
        decision = self.router(
            [
                SystemMessage(
                    content="Route the input to story, joke, or poem based on the user's request.  If it is not clear, choose clarify."
                ),
                HumanMessage(content=state["input"]),
            ]
        )
        
        print(f"DEBUG -> DECISION = {decision}")
        return {"decision": decision.step}
    
class OrchestratorNodes(ClaudeNodes):
    
    @property
    def user_prompt(self):
        print("DEBUG -> Executing node: user_prompt (OrchestratorNodes)")
        return ReportPrompt()

    def orchestrator(self, state: OrchestratorState):
        print("DEBUG -> Executing node: orchestrator")
        """Orchestrator that generates a plan for the report"""
        # Generate queries
        report_sections = self.planner(
            [
                SystemMessage(content="Generate a plan for the report."),
                HumanMessage(content=f"Here is the report topic: {state['topic']}"),
            ]
        )
        return {"sections": report_sections.sections}

    def section_writer(self, state: WorkerState):
        section_name = state['section'].name
        description = state['section'].description
        print(f"DEBUG -> Executing node: (section_writer)\n--------\n     section_name: {section_name}\n     description: {description}\n--------\n")
        """Worker writes a section of the report"""
        
        # Generate section
        section = self.LLM.sonnet.invoke(
            [
                SystemMessage(
                    content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."
                ),
                HumanMessage(
                    content=f"Here is the section name: {state['section'].name} and description: {state['section'].description}"
                ),
            ]
        )
        # Write the updated section to completed sections
        return {"completed_sections": [section.content]}

    def synthesizer(self, state: OrchestratorState):
        print("DEBUG -> Executing node: synthesizer")
        """Synthesize full report from sections"""
        # List of completed sections
        completed_sections = state["completed_sections"]
        
        print(f"DEBUG -> completed_sections: {completed_sections}")
        # Format completed section to str to use as context for final sections
        completed_report_sections = "\n\n---\n\n".join(completed_sections)
        print(f"DEBUG -> final_report: {completed_report_sections}")
        
        return {"final_report": completed_report_sections}

    def assign_workers(self, state: OrchestratorState):
        print("DEBUG -> Executing node: assign_workers")
        """Assign a worker to each section in the plan"""
        # Kick off section writing in parallel via Send() API
        return [Send("section_writer", {"section": s}) for s in state["sections"]]
