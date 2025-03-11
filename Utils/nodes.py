# Nodes
from abc import ABC, abstractmethod
from dataclasses import dataclass
from langchain.schema import SystemMessage, HumanMessage
from Utils.states import JokeGeneratorState, ParallelWorkflowState, RoutingState
from Utils.structured_outputs import JokeResponse, PoemResponse, StoryResponse
from config import MODELS

@dataclass
class Prompt:
    text: str
    var: str

@dataclass
class JokePrompt(Prompt):
    text: str = "Enter a topic for your joke: "
    var: str = "topic"

@dataclass
class ContentPrompt(Prompt):
    text: str = "Enter a topic for your content: "
    var: str = "topic"
    
@dataclass
class RequestPrompt(Prompt):
    text: str = "Enter a topic for your content: "
    var: str = "topic"

class ClaudeNodes(ABC):
    LLM: str = MODELS.Anthropic.Claude_3_5
    PROMPT: str = "Axovia> "
        
    @property
    @abstractmethod
    def user_prompt(self) -> Prompt:
        raise NotImplementedError("User prompt not implemented")
    
    @property
    def joke_generator(self): return self.LLM.joke_gen.invoke

    @property
    def story_generator(self): return self.LLM.story_gen.invoke

    @property
    def poem_generator(self): return self.LLM.poem_gen.invoke

    def output(self, msg: str):
        print(f"{self.PROMPT} {msg}")

    def prompt_user(self, state: JokeGeneratorState) -> str:
        """Prompt user for joke topic"""
        response = input(f"Axovia> {self.user_prompt.text}: ")
        return {self.user_prompt.var: response}


# Nodes
class JokeGeneratorNodes(ClaudeNodes):
    
    @property
    def user_prompt(self): return JokePrompt()
    
    def generate_joke(self, state: JokeGeneratorState) -> str:
        self.output("Generating joke....")
        msg = self.joke_generator(f"Write a short joke about {state['topic']}")
        print(f"generated joke output: {msg}")
        return {"joke": msg.joke}
    
    def improve_joke(self, state: JokeGeneratorState) -> str:
        self.output("Improving joke....")
        msg = self.joke_generator(f"Make this joke funnier by adding wordplay: {state['joke']}")
        return {"improved_joke": msg.joke}
    
    def polish_joke(self, state: JokeGeneratorState) -> str:
        self.output("Polishing joke....")
        msg = self.joke_generator(f"Add a surprising twist to this joke: {state['improved_joke']}")
        return {"final_joke": msg.joke}

    
class ParallelWorkflowNodes(ClaudeNodes):
    
    @property
    def user_prompt(self): return ContentPrompt()

    def split(self, state: ParallelWorkflowState):
        """Split the workflow into three parallel LLM calls"""
        print(f"DEBUG -> split")
        return {"topic": state["topic"]}

    def create_joke(self, state: ParallelWorkflowState):
        print(f"DEBUG -> joke")
        msg = self.joke_generator(f"Write a joke about {state['topic']}")
        return {"joke": msg.joke}
    
    def create_story(self, state: ParallelWorkflowState):
        print(f"DEBUG -> story")
        msg = self.story_generator(f"Write a story about {state['topic']}")
        return {"story": msg.story}
    
    def create_poem(self, state: ParallelWorkflowState):
        print(f"DEBUG -> poem")
        msg = self.poem_generator(f"Write a poem about {state['topic']}")
        return {"poem": msg.poem}

    def aggregator(self, state: ParallelWorkflowState):
        """Combine the joke, story and poem into a single output"""
        
        combined = f"Here's a story, joke and poem about {state['topic']}!\n\n"
        combined += f"STORY: {state['story']}\n"
        combined += f"JOKE: {state['joke']}\n"
        combined += f"POEM: {state['poem']}"
        return {"combined_output": combined}


class RoutingNodes(ClaudeNodes):

    @property
    def user_prompt(self): return RequestPrompt()

    # Nodes
    def llm_call_1(state: RoutingState):
        """Write a story"""

        result = llm.invoke(state["input"])
        return {"output": result.content}


    def llm_call_2(state: RoutingState):
        """Write a joke"""

        result = llm.invoke(state["input"])
        return {"output": result.content}


    def llm_call_3(state: RoutingState):
        """Write a poem"""

        result = llm.invoke(state["input"])
        return {"output": result.content}


    def llm_call_router(state: RoutingState):
        """Route the input to the appropriate node"""

        # Run the augmented LLM with structured output to serve as routing logic
        decision = router.invoke(
            [
                SystemMessage(
                    content="Route the input to story, joke, or poem based on the user's request."
                ),
                HumanMessage(content=state["input"]),
            ]
        )

        return {"decision": decision.step}