from news_ai.llm.planner import llm
from news_ai.instructor.instructions import analysis_instruction
from langchain_core.messages import SystemMessage, HumanMessage

analyser = llm

def analyser(news: dict):
    analysis = analyser.invoke(
        [
            SystemMessage(content=analysis_instruction),
            HumanMessage(
                content=f"Here is the news details: {news}"
            ),
        ]
    )

    return analysis.content