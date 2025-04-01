from langgraph.constants import Send
from news_ai.instructor.instructions import orchestration_instruction, news_instruction, analysis_instruction, explainer_instruction, worker_instruction
from news_ai.structure.schema import WorkerState, State, ExplainerState
from news_ai.llm.planner import planner, llm, newsai, llm_2
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.utilities import GoogleSerperAPIWrapper
from news_ai.db.db import get_rss_news
from news_ai.logging.logger import logging
from news_ai.exception_handler.exception import NewsException
import sys

# Nodes
def google_news(topic: str):
    logging.info("Entered in Google News")
    try:
        search = GoogleSerperAPIWrapper(type="news", tbs="qdr:h24")
        results = search.results(topic)
        
        for news in results["news"]:
            for key in ['imageUrl', 'position', 'snippet']:
                if key in news:
                    del news[key] 

            return results['news'] 
    except Exception as e:
        raise NewsException(e, sys)

def news(topic: str):
    logging.info("Entered in News") 
    try:
        g_news = google_news(topic)
        r_news = get_rss_news(keyword=topic)
        logging.info(f"r_news = {r_news}")
        latest_news = g_news + r_news
        return latest_news
    except Exception as e:
        raise NewsException(e, sys)

def news_ai(state: State):
    """AI agent that understand user query and generate string for news extraction"""
    logging.info("Entered in News AI")
    try:
        news_topic = newsai.invoke(
            [
            SystemMessage(content=news_instruction),
            HumanMessage(
                content=f"Here is the user query: {state['news_topic']}"
            ),
        ]
    )

        topic = news_topic.news_topic
        logging.info(f"topic = {topic}")
        latest_news = news(topic=topic)
        logging.info(f"latest_news = {latest_news}")
        return {"latest_news": latest_news}
    except Exception as e:
        raise NewsException(e, sys)
    

def orchestrator(state: State):
    """Orchestrator that generates a plan for the news"""
    logging.info(f"Entered in Orchestrator: {state['latest_news']}")
    try:
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
    except Exception as e:
        raise NewsException(e, sys)

def llm_call(state: WorkerState):
    """Worker writes a section of the report"""
    logging.info("Entered in LLM Call")
    try:
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
    except Exception as e:
        raise NewsException(e, sys)


def synthesizer(state: State):
    """Synthesize full report from sections"""
    logging.info("Entered in Synthesizer")
    try:
        # List of completed sections
        completed_sections = state["completed_sections"]

        completed_report_sections = "\n\n---\n\n".join(completed_sections)

        return {"final_report": completed_report_sections}
    except Exception as e:
        raise NewsException(e, sys)


# Conditional edge function to create llm_call workers that each write a section of the report
def assign_workers(state: State):
    """Assign a worker to each section in the plan"""
    #print([s for s in state["sections"]])
    # Kick off section writing in parallel via Send() API
    return [Send("llm_call", {"section": s}) for s in state["sections"]]

def explainer(state: ExplainerState):
    logging.info("Entered in Explainer")
    try:
        explainer = llm_2
        response = explainer.invoke(
        [
            SystemMessage(content=explainer_instruction),
            HumanMessage(
                content=f"Here is the question: {state['question']}"
            ),
        ]
    )
    
        return {"answer": response.content}
    except Exception as e:
        raise NewsException(e, sys)
