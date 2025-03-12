import dotenv
from langchain_anthropic import ChatAnthropic
from Utils.tools import multiply

from Utils.structured_outputs import SearchQuery
from config import MODELS

llm = MODELS.Anthropic.claude_3_5

llm_with_tools = llm.bind_tools((multiply))

msg = llm_with_tools.invoke("What is 2 times 3?")

print(msg.tool_calls)
