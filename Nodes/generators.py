from dataclasses import dataclass
from typing import Tuple
from Nodes.axovia import AxoviaNode
from Utils.constants import MODELS
from Utils.states import JokeGeneratorState, WorkflowState


class GeneratorNode(AxoviaNode):
    
    def method(self, state: WorkflowState) -> dict[str, str]:
        input_value = state.get(self.state_input[0], "")
        formatted_prompt = self.prompt.format(input_value)
        result = self.model.invoke(formatted_prompt)
        return {self.state_output: result.joke}

            
class JokeGeneratorNode(GeneratorNode):
    def __init__(self):
        self.model: object = MODELS.Anthropic.claude_3_5.joke_gen
        super().__init__()

        
class GenerateJoke(JokeGeneratorNode):
        name: str = "generate_joke"
        state_input: Tuple[str] = ("topic",)
        state_output: str = "joke"
        prompt: str = "Write a short joke about {state_input}"


class ImproveJoke(JokeGeneratorNode):
        name: str = "improve_joke"
        state_input: Tuple[str] = ("joke",)
        state_output: str = "improved_joke"
        prompt: str = "Make this joke funnier by adding wordplay: {state_input}"

        
class FinalizeJoke(JokeGeneratorNode):
        name = "finalize_joke"
        state_input = ("improved_joke",)
        state_output = "final_joke"
        prompt = "Add a surprising twist to this joke: {state_input}"
        
# class StoryGeneratorNode(GeneratorNode):
#     model: object = MODELS.Anthropic.claude_3_5.story_gen

# class PoemGeneratorNode(GeneratorNode):
#     model: object = MODELS.Anthropic.claude_3_5.poem_gen
    
# class CreateStory(StoryGeneratorNode):
#     name: str = "create_story"
#     gen_var: str = "story"
#     def __init__(self, state: JokeGeneratorState):
#         self.prompt: str = f"Write a story about {state['topic']}"

# class CreatePoem(PoemGeneratorNode):
#     name: str = "create_poem"
#     gen_var: str = "poem"
#     def __init__(self, state: JokeGeneratorState):
#         self.prompt: str = f"Write a poem about {state['topic']}"

## Modifiers 

# # Nodes
# @dataclass
# class JokeGeneratorNodes(BaseModel):
#     user_prompt: Prompt = JokePrompt()
#     generate_joke: FunctionType = lambda state: GenerateJoke(state)
#     improve_joke: FunctionType = lambda state: ImproveJoke(state)
#     finalize_joke: FunctionType = lambda state: FinalizeJoke(state)

#     # def generate_joke(self, state: JokeGeneratorState) -> str:
#     #     print("DEBUG -> Executing node: generate_joke")
#     #     self.output("Generating joke....")
#     #     msg = self.joke_generator(f"Write a short joke about {state['topic']}")
#     #     print(f"generated joke output: {msg}")
#     #     return {"joke": msg.joke}
    
#     # def improve_joke(self, state: JokeGeneratorState) -> str:
#     #     msg = self.joke_generator(f"Make this joke funnier by adding wordplay: {state['joke']}")
#     #     return {"improved_joke": msg.joke}
    
#     # def polish_joke(self, state: JokeGeneratorState) -> str:
#     #     msg = self.joke_generator(f"Add a surprising twist to this joke: {state['improved_joke']}")
#     #     return {"final_joke": msg.joke}
