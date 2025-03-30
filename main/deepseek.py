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

# call APIs
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"]=os.getenv("LANGSMITH_PROJECT")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")


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
import datetime

# API configurations
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Page Config
st.set_page_config(
    page_title="News AI", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Styling
st.markdown("""
    <style>
        :root {
            --primary: #4a6fa5;
            --secondary: #166088;
            --accent: #4fc3f7;
            --background: #0f172a;
            --card-bg: #1e293b;
            --text: #f8fafc;
        }
        
        body {
            background-color: var(--background);
            color: var(--text);
        }
        
        .main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .title-container {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        
        .title {
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(90deg, #f8fafc, #e2e8f0);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-top: 0.5rem;
        }
        
        .news-card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            border-left: 4px solid var(--accent);
        }
        
        .news-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        }
        
        .news-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--accent);
        }
        
        .news-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 1rem;
        }
        
        .news-content {
            line-height: 1.6;
        }
        
        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(79,195,247,0.5), transparent);
            margin: 1.5rem 0;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 0.8rem 2rem;
            border-radius: 50px;
            border: none;
            margin: 1rem auto;
            display: block;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        }
        
        .sidebar .sidebar-content {
            background-color: var(--card-bg);
        }
        
        .timestamp {
            font-size: 0.8rem;
            text-align: right;
            opacity: 0.7;
            margin-top: 1rem;
        }
        
        .tag {
            display: inline-block;
            background-color: rgba(79,195,247,0.2);
            color: var(--accent);
            padding: 0.3rem 0.8rem;
            border-radius: 50px;
            font-size: 0.8rem;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .main {
                padding: 1rem;
            }
            
            .title {
                font-size: 2rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Function to process AI news
def process_ai_news():
    response = orchestrator_worker.invoke({"news_topic": "AI"})
    explanation = response.get("final_report", "No response received.")
    return explanation

# Function to parse the news report into individual articles
def parse_news_report(report):
    articles = []
    sections = report.split('\n---\n')
    for section in sections:
        if not section.strip():
            continue
            
        title = ""
        source = ""
        timestamp = ""
        content = ""
        
        lines = section.split('\n')
        for line in lines:
            if line.startswith('## '):
                title = line[3:].strip()
            elif line.startswith('**Source**:'):
                source = line.split('**Source**:')[1].strip()
            elif line.startswith('**Timestamp**:'):
                timestamp = line.split('**Timestamp**:')[1].strip()
            else:
                content += line + '\n'
        
        if title:
            articles.append({
                'title': title,
                'source': source,
                'timestamp': timestamp,
                'content': content.strip()
            })
    
    return articles

# Sidebar
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("### Categories")
    st.checkbox("Technology", value=True)
    st.checkbox("Business", value=True)
    st.checkbox("Science", value=True)
    st.checkbox("Politics", value=True)
    
    st.markdown("### Time Range")
    time_range = st.selectbox("Select time range", ["Last 24 hours", "Last week", "Last month"])
    
    st.markdown("### Sources")
    st.checkbox("The New York Times", value=True)
    st.checkbox("WIRED", value=True)
    st.checkbox("TechCrunch", value=True)
    st.checkbox("MIT Technology Review", value=True)
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("[AI Research Papers](https://arxiv.org/)")
    st.markdown("[Tech News Aggregator](https://techmeme.com/)")
    st.markdown("[AI Ethics Resources](https://futureoflife.org/)")

# Main Content
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="title-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">🤖 News AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your personalized AI-powered news aggregator</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Search and Refresh
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search for specific AI topics...", placeholder="e.g. 'AI ethics', 'machine learning', 'neural networks'")
    with col2:
        if st.button("🔄 Refresh News"):
            st.experimental_rerun()
    
    # Main Button
    if st.button("📰 Get Latest AI News Analysis", key="main_button"):
        with st.spinner("🤖 Our AI is analyzing the latest news across the web..."):
            try:
                news_report = process_ai_news()
                articles = parse_news_report(news_report)
                
                st.success(f"✅ Successfully analyzed {len(articles)} articles")
                st.markdown(f'<div class="timestamp">Last updated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
                
                # Display tags
                st.markdown("### 🔖 Popular Topics")
                st.markdown('<span class="tag">AI Ethics</span><span class="tag">Machine Learning</span><span class="tag">Neural Networks</span><span class="tag">Computer Vision</span><span class="tag">Natural Language Processing</span>', unsafe_allow_html=True)
                
                # Display articles
                for article in articles:
                    st.markdown('<div class="news-card">', unsafe_allow_html=True)
                    st.markdown(f'<h3 class="news-title">{article["title"]}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<div class="news-meta"><span>📰 {article["source"]}</span><span>⏱️ {article["timestamp"]}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="news-content">{article["content"]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error("🚨 An error occurred while processing the news.")
                st.error(str(e))

    st.markdown('</div>', unsafe_allow_html=True)

# # Page Config
# st.set_page_config(page_title="News AI", page_icon="🤖", layout="centered")

# # Custom CSS for Styling
# st.markdown("""
#     <style>
#         .main {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#         }
#         .title {
#             text-align: center;
#             font-size: 48px;
#             font-weight: 700;
#             margin-top: 40px;
#             margin-bottom: 20px;
#             color: white;
#         }
#         .stButton>button {
#             background-color: #1f77b4;
#             color: white;
#             font-size: 20px;
#             padding: 10px 24px;
#             border-radius: 12px;
#             border: none;
#             margin-top: 20px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Function to simulate AI pipeline processing (replace this with your orchestrator_worker logic)
# def process_ai_news():
#     response = orchestrator_worker.invoke({"news_topic": "AI"})
#     #print(response)
#     explaination = response.get("final_report", "No response received.")  # Adjust based on your agent output
#     return explaination

# # Centered Container
# with st.container():
#     st.markdown('<div class="main">', unsafe_allow_html=True)
#     st.markdown('<div class="title">🤖 News AI</div>', unsafe_allow_html=True)

#     if st.button("📰 Get Latest AI News"):
#         with st.spinner("Fetching and summarizing the latest AI news..."):
#             try:
#                 news_report = process_ai_news()
#                 st.success("🧠 Here's your curated AI news summary:")
#                 st.write(news_report)
#             except Exception as e:
#                 st.error("🚨 An error occurred while processing the news.")
#                 #st.exception(e)

#     st.markdown('</div>', unsafe_allow_html=True)

