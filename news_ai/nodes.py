from langgraph.constants import Send
from news_ai.instructions import orchestration_instruction, worker_instruction
from news_ai.schema import WorkerState, State
from news_ai.planner import planner, llm
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.utilities import GoogleSerperAPIWrapper

# Nodes
def news(topic: str):
    search = GoogleSerperAPIWrapper(type="news", tbs="qdr:h24")
    results = search.results(topic)
    
    for news in results["news"]:
        for key in ['imageUrl', 'position']:
            if key in news:
                del news[key] 
 
    return results['news']

def orchestrator(state: State):
    """Orchestrator that generates a plan for the news"""

    latest_news = news(state["news_topic"])

    # Generate queries
    report_sections = planner.invoke(
        [
            SystemMessage(content=orchestration_instruction),
            HumanMessage(
                content=f"Here is the latest AI news: {latest_news}"
            ),
        ]
    )
  

    return {"sections": report_sections.sections}

def llm_call(state: WorkerState):
    """Worker writes a section of the report"""

    # Generate section
    section = llm.invoke(
        [
            SystemMessage(content=worker_instruction),
            HumanMessage(
                content=f"Here is the news_title: {state['section'].title},\
                      news_link: {state['section'].link}, time_published: {state['section'].time_published},\
                          news_source: {state['section'].source}" # news_snippet: {state['section'].snippet}
            ),
        ]
    )

    return {"completed_sections": [section.content]}


def synthesizer(state: State):
    """Synthesize full report from sections"""

    # List of completed sections
    completed_sections = state["completed_sections"]
  
    completed_report_sections = "\n\n---\n\n".join(completed_sections)

    return {"final_report": completed_report_sections}


# Conditional edge function to create llm_call workers that each write a section of the report
def assign_workers(state: State):
    """Assign a worker to each section in the plan"""
    return [Send("llm_call", {"section": s}) for s in state["sections"]]
