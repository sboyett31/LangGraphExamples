from Utils.structured_outputs import SearchQuery
from config import MODELS

llm = MODELS.Anthropic.claude_3_5

structured_llm = llm.with_structured_output(SearchQuery)

output = structured_llm.invoke("How does Calicum CT score relate to high cholestorol")

print(output.search_query)
print(output.justification)

