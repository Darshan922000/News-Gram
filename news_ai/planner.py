from langchain_groq import ChatGroq
from news_ai.schema import Sections, query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

llm = ChatGroq(model="gemma2-9b-it")

# Augment the LLM with schema for structured output
planner = llm.with_structured_output(Sections)

newsai = llm.with_structured_output(query)
