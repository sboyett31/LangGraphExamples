from dataclasses import dataclass, field
from Nodes.axovia import AxoviaNode
from Utils.constants import MODELS
from Utils.states import WorkflowState
from Utils.types import Prompt
    
class PromptUser(AxoviaNode):
    name: str = "prompt_user"
    user_prompt: Prompt = Prompt(text="Enter input: ", var="input")

    def method(self, state: WorkflowState) -> dict[str, str]:
        # Get user input
        result = input(self.user_prompt["text"])
        return {self.user_prompt["var"]: result}

class JokePrompt(PromptUser):
    name: str = "prompt_user"
    user_prompt: Prompt = Prompt(text="Enter a topic for your joke: ", var="topic")
