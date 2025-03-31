from langgraph.constants import Send
from news_ai.instructions import orchestration_instruction, worker_instruction, news_instruction
from news_ai.schema import WorkerState, State
from news_ai.planner import planner, llm, newsai
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.utilities import GoogleSerperAPIWrapper
from news_ai.db import get_rss_news

# Nodes
def google_news(topic: str):
    search = GoogleSerperAPIWrapper(type="news", tbs="qdr:h24")
    results = search.results(topic)
    #pprint.pp(results)
    
    for news in results["news"]:
        for key in ['imageUrl', 'position', 'snippet']:
            if key in news:
                del news[key] 

    #pprint.pp(results)
    return results['news'] 

def news(topic: str):
    g_news = google_news(topic)
    r_news = get_rss_news(keyword=topic)
    print("r_news = ",r_news)
    latest_news = g_news + r_news
    return latest_news

def news_ai(state: State):
    """AI agent that understand user query and generate string for news extraction"""

    news_topic = newsai.invoke(
        [
            SystemMessage(content=news_instruction),
            HumanMessage(
                content=f"Here is the user query: {state['news_topic']}"
            ),
        ]
    )
    # news_topic_dict = news_topic.model_dump()
    # print("news_topic:", news_topic_dict)

    topic = news_topic.news_topic
    latest_news = news(topic=topic)
    print("latest =", latest_news)
    return {"latest_news": latest_news}


def orchestrator(state: State):
    """Orchestrator that generates a plan for the news"""

    report_sections = planner.invoke(
        [
            SystemMessage(content=orchestration_instruction),
            HumanMessage(
                content=f"Here is the latest AI news: {state['latest_news']}"
            ),
        ]
    )

    print("Report Sections:",report_sections)

    return {"sections": report_sections.sections}

def llm_call(state: WorkerState):
    """Worker writes a section of the report"""

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

    completed_sections = state["completed_sections"]

    completed_report_sections = "\n\n---\n\n".join(completed_sections)

    return {"final_report": completed_report_sections}


# Conditional edge function to create llm_call workers that each write a section of the report
def assign_workers(state: State):
    """Assign a worker to each section in the plan"""
    #print([s for s in state["sections"]])
    # Kick off section writing in parallel via Send() API
    return [Send("llm_call", {"section": s}) for s in state["sections"]]