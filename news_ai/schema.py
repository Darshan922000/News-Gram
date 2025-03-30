from typing import Annotated, List
import operator
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

class Section(BaseModel):
    title: str = Field(
        description="A title of the news",
    )
    link: str = Field(
        description="A link to the news",
    )
    time_published: str = Field(
        description="A time when news published",
    )
    source: str = Field(
        description="A news chennel name",
    )

class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the AI news",
    )

# Graph state
class State(TypedDict):
    news_topic: str  # news topic
    sections: list[Section]  # List of news sections
    completed_sections: Annotated[list, operator.add]  # All workers write to this key in parallel
    final_report: str  # Final report

# Worker state
class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]
