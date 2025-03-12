## Constants for the Axovia Agentic Workflows Project

# Supported Node Types
import os
from langchain_anthropic import ChatAnthropic

from Utils.structured_outputs import JokeResponse #, PoemResponse, Route, Sections, StoryResponse


SUPPORTED_NODETYPES = [
    "Swarm", 
    "Evaluator", 
    "Planner", 
    "Router", 
    "Generator", 
    "Worker"
]

class MODELS:
    class Anthropic:
        # Change Claude_3_5 to claude_3_5 to match usage in other files
        class claude_3_5:
            sonnet = ChatAnthropic(
                model="claude-3-5-sonnet-latest",
                anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY")
            )
            joke_gen = sonnet.with_structured_output(JokeResponse)
            # story_gen = sonnet.with_structured_output(StoryResponse)
            # poem_gen = sonnet.with_structured_output(PoemResponse)
            # router = sonnet.with_structured_output(Route)
            # planner = sonnet.with_structured_output(Sections)
