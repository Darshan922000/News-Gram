from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from news_ai.structure.schema import Sections, query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

llm = ChatGroq(model="gemma2-9b-it")


#llm_2 = ChatGroq(model="llama-3.1-8b-instant") # qwen-2.5-32b

# Augment the LLM with schema for structured output
planner = llm.with_structured_output(Sections)

newsai = llm.with_structured_output(query)
