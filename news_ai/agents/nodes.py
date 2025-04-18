from langgraph.constants import Send
from news_ai.instructor.instructions import orchestration_instruction, news_instruction, explainer_instruction, worker_instruction
from news_ai.structure.schema import WorkerState, State, ExplainerState
from news_ai.llm.planner import planner, llm, newsai
from langchain_core.messages import SystemMessage, HumanMessage
from news_ai.logging.logger import logging
from news_ai.exception_handler.exception import NewsException
import sys
from news_ai.agents.functions import news, sanitize_news_list
import os
from dotenv import load_dotenv
load_dotenv()


os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"]=os.getenv("LANGSMITH_PROJECT")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Nodes
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
        latest_news = latest_news[0:10]
        #latest_news = [{'title': "Is Musk nearing the end at DOGE? 'At some point, he's going to be going back,' Trump says.", 'link': 'https://www.usatoday.com/story/news/politics/2025/04/01/trump-elon-musk-leave-white-house-doge/82754394007/', 'date': '11 minutes ago', 'source': 'USA Today'}, {'title': '"I ll pay for his coach flight": Democrats beg Elon Musk to campaign for their GOP foes', 'link': 'https://www.axios.com/2025/04/03/elon-musk-house-democrats-wisconsin-election', 'date': '51 minutes ago', 'source': 'Axios'}, {'title': "As Elon Musks popularity declines, what is his likely future in GOP politics?", 'link': 'https://www.npr.org/2025/04/03/nx-s1-5349452/as-elon-musks-popularity-declines-what-is-his-likely-future-in-gop-politics', 'date': '2 hours ago', 'source': 'NPR'}, {'title': 'Elon Musk took a Gold Card out of his ass and gave it to me!', 'link': 'https://www.dailycardinal.com/article/2025/04/elon-musk-took-a-gold-card-out-of-his-ass-and-gave-it-to-me', 'date': '3 hours ago', 'source': 'The Daily Cardinal'}, {'title': 'Elon Musk: X is suing India, as Tesla and Starlink plan entry', 'link': 'https://www.bbc.com/news/articles/cpv4974k27wo', 'date': '7 hours ago', 'source': 'BBC'}, {'title': 'For Trump, Elon Musk Is a Liability, but Still Useful for Now', 'link': 'https://www.nytimes.com/2025/04/02/us/politics/trump-musk-wisconsin.html', 'date': '10 hours ago', 'source': 'The New York Times'}, {'title': 'Democrats� win in Wisconsin court race also is a big loss for Elon Musk', 'link': 'https://apnews.com/article/wisconsin-supreme-court-elon-musk-81f71cdda271827ae281a77072a26bad', 'date': '11 hours ago', 'source': 'AP News'}, {'title': 'Trump Tells Inner Circle That Musk Will Leave Soon', 'link': 'https://www.politico.com/news/magazine/2025/04/02/trump-musk-leaving-political-liability-00265784', 'date': '15 hours ago', 'source': 'Politico'}, {'title': 'Tesla sales plunge: Biggest decline in history', 'link': 'https://www.cnn.com/2025/04/02/business/tesla-sales/index.html', 'date': '16 hours ago', 'source': 'CNN'}, {'title': 'Trump privately indicates Musk to step back from administration after government employee status expires: Sources', 'link': 'https://abcnews.go.com/US/trump-privately-elon-musk-step-back-current-role/story?id=120415238', 'date': '17 hours ago', 'source': 'ABC News'}]
        latest_news = sanitize_news_list(latest_news)
        logging.info(f"latest_news = {latest_news}, length = {len(latest_news)}")
        return {"latest_news": latest_news}
    except Exception as e:
        raise NewsException(e, sys)
    
# def verification_ai(state: State):
#     """AI agent that understand user query and generate string for news extraction"""
#     logging.info("Entered in Verification AI")
#     try:
#         clean_news = llm_2.invoke(
#             [
#             SystemMessage(content=verification_instruction),
#             HumanMessage(
#                 content=f"Here is the user query: {state['latest_news']}"
#             ),
#         ]
#     )
#         logging.info(f"clean_news = {clean_news}")
#         return {"latest_news": clean_news}
#     except Exception as e:
#         raise NewsException(e, sys)

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
        #print("Report Sections:",report_sections)

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
                      news_link: {state['section'].link}, time_published: {state['section'].date},\
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
        explainer = llm
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
