from typing import List, Literal
from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query that is optimized web search.")
    justification: str = Field(None, justification="Why this query is relevant to the user's request.")

class Route(BaseModel):
    step: Literal["poem", "story", "joke", "clarify"] = Field(
        None, description="The next step in the routing process."
    )

class JokeResponse(BaseModel):
    joke: str = Field(None, description="The generated joke.")

class StoryResponse(BaseModel):
    story: str = Field(None, description="The generated story.")
    
class PoemResponse(BaseModel):
    poem: str = Field(None, description="The generated poem.")


# Schema for structured output to use in planning
class Section(BaseModel):
    name: str = Field(
        description="Name for this section of the report.",
    )
    description: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this section.",
    )

class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the report.",
    )
