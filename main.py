from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.messages import HumanMessage
from news_ai.system.graph import synth_mind, help_search

# Create FastAPI app
app = FastAPI(
    title="News AI API",
    description="API for searching news and getting help explanations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class NewsSearchRequest(BaseModel):
    topic: str

class HelpRequest(BaseModel):
    query: str

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to News AI API"}

@app.post("/news_search")
async def search_news(request: NewsSearchRequest):
    try:
        news = synth_mind()
        results = news.invoke({"news_topic": request.topic})
        return {"news": results["final_report"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching news: {str(e)}")

@app.post("/help_search")
async def analyze_news(request: HelpRequest):
    try:

        support = help_search()
        result = support.invoke({"question": request.query})
        print(result["answer"])
        return {"report": result["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing news: {str(e)}")


# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
