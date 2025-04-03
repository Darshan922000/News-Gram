from typing import Annotated, List, Any
import operator
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

class Section(BaseModel):
    title: Any = Field(
        description="A title of the news",
    )
    link: Any = Field(
        description="A link to the news",
    )
    date: Any = Field(
        description="A time when news published",
    )
    source: Any = Field(
        description="A news chennel name",
    )

class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the AI news",
    )

# Graph state
class State(TypedDict):
    news_topic: str  # news topic
    latest_news: list[dict]
    sections: list[Section]  # List of news sections
    completed_sections: Annotated[list, operator.add]  # All workers write to this key in parallel
    final_report: str  # Final report

class ExplainerState(TypedDict):
    question: str
    answer: str

# Worker state
class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]

class query(BaseModel):
    news_topic: str = Field(description="string for topic")
