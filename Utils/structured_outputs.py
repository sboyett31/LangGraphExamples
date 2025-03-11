from typing import Literal
from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query that is optimized web search.")
    justification: str = Field(None, justification="Why this query is relevant to the user's request.")

class RouterResponse(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(
        None, description="The next step in the routing process"
    )

class JokeResponse(BaseModel):
    joke: str = Field(None, description="The generated joke.")

class StoryResponse(BaseModel):
    story: str = Field(None, description="The generated story.")
    
class PoemResponse(BaseModel):
    poem: str = Field(None, description="The generated poem.")
