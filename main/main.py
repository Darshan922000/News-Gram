from fastapi import FastAPI
import os
from pydantic import BaseModel
from langgraph.graph.message import MessagesState
import uvicorn
from IPython.display import Markdown
from news_ai.graph import orchestrator_worker
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import time

# Configure APIs
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Page Config with wider layout and custom theme
st.set_page_config(
    page_title="News AI - Your AI News Curator",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
        :root {
            --primary: #6C63FF;
            --secondary: #4D44DB;
            --accent: #FF6584;
            --dark: #2D3748;
            --light: #F7FAFC;
            --gray: #A0AEC0;
        }
        
        .main {
            max-width: none;
            padding: 2rem 5%;
        }
        
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #1f77b4;
        }

        .stButton>button {
            background-color: #1f77b4;
            color: white;
            font-size: 18px;
            border-radius: 10px;
        }
        
        .summary-container {
            display: flex;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .summary-card {
            background: #1A1A2E;
            border-radius: 12px;
            padding: 2rem;
            color: white;
            border-left: 4px solid var(--accent);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            flex: 2;  /* Takes more space */
        }
        
        .summary-sidebar {
            flex: 1;  /* Takes less space */
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 1.5rem;
            border-left: 4px solid var(--primary);
        }
        
        .summary-content {
            line-height: 1.7;
            font-size: 1.1rem;
        }
        
        .summary-content h1 {
            font-size: 1.8rem !important;
            margin: 0 0 1rem 0 !important;
        }
        
        .summary-content h2 {
            font-size: 1.4rem !important;
            margin: 1.5rem 0 0.8rem 0 !important;
        }
        
        .summary-content h3 {
            font-size: 1.2rem !important;
            margin: 1.2rem 0 0.6rem 0 !important;
        }
        
    </style>
""", unsafe_allow_html=True)



# Function to process AI news with simulated steps
def process_ai_news(topic):
    # Simulate processing steps with progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "🔍 Searching for latest news articles...",
        "📚 Analyzing and summarizing content...",
        "🧠 Identifying key insights and trends...",
        "✍️ Crafting comprehensive report...",
        "✅ Finalizing output..."
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(1)  # Simulate processing time
    
    try:
        # Actual processing
        response = orchestrator_worker.invoke({"news_topic": "AI"})
        return response.get("final_report", "No response received.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# App Title
st.markdown('<h1 class="title">🤖 News AI</h1>', unsafe_allow_html=True)


news_topic = "AI"
if st.button(f"📡 Get Latest {news_topic} News", key="main_button"):
    with st.spinner(""):
        news_report = process_ai_news(news_topic)
            
        if news_report:
            #st.success("## 🎉 Your AI-Generated News Report")
                
            # Display the report in the new dark card
            st.markdown(f"""
                <div class="summary-card">
                    <div class="summary-title">📌 {news_topic} News Summary</div>
                    <div class="summary-content">{news_report}</div>
                </div>
            """, unsafe_allow_html=True)
                


