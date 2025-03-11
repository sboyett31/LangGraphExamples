from Utils.structured_outputs import JokeResponse, PoemResponse, RouterResponse, StoryResponse
import dotenv
import os
from langchain_anthropic import ChatAnthropic

# Load environment variables immediately
def init_env():
    dotenv.load_dotenv(".env")

# Call init_env at import time to ensure environment variables are loaded
init_env()

class MODELS:
    class Anthropic:
        class Claude_3_5:
            sonnet = ChatAnthropic(
                model="claude-3-5-sonnet-latest",
                anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY")
            )
            joke_gen = sonnet.with_structured_output(JokeResponse)
            story_gen = sonnet.with_structured_output(StoryResponse)
            poem_gen = sonnet.with_structured_output(PoemResponse)
            router = sonnet.with_structured_output(RouterResponse)
