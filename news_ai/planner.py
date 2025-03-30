from langchain_groq import ChatGroq
from news_ai.schema import Sections
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

llm = ChatGroq(model="deepseek-r1-distill-qwen-32b")

# Augment the LLM with schema for structured output
planner = llm.with_structured_output(Sections)
