"""FastAPI application for Employee Policy Q&A System"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_pipeline import RAGPipeline
from src.qa_system import QASystem

# Initialize FastAPI app
app = FastAPI(
    title="Employee Policy Q&A System",
    description="RAG-based Q&A system for employee policies",
    version="1.0.0"
)

# CORS middleware
import os
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline and QA system
print("Initializing RAG pipeline...")
pipeline = RAGPipeline()

# Check if documents are ingested
store_info = pipeline.vector_store.get_collection_info()
if store_info.get("document_count", 0) == 0:
    print("No documents found. Running ingestion...")
    pipeline.ingest_documents()

qa_system = QASystem(pipeline)
print("Q&A System ready!")


# Pydantic models
class QuestionRequest(BaseModel):
    question: str


class SourceResponse(BaseModel):
    source: str
    relevance_score: float


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceResponse]
    confidence: float


# API Routes
@app.get("/")
async def read_root():
    """Serve the frontend HTML file"""
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "vector_store": pipeline.vector_store.get_collection_info()
    }


@app.post("/api/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer"""
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Get answer from QA system
        result = qa_system.answer(request.question.strip())
        
        # Format response
        sources = [
            SourceResponse(
                source=source["source"],
                relevance_score=source["relevance_score"]
            )
            for source in result["sources"]
        ]
        
        return AnswerResponse(
            question=result["question"],
            answer=result["answer"],
            sources=sources,
            confidence=result["confidence"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    store_info = pipeline.vector_store.get_collection_info()
    return {
        "documents_in_store": store_info.get("document_count", 0),
        "vector_db_type": store_info.get("type", "Unknown"),
        "embedding_model": "text-embedding-ada-002",
        "llm_model": "gpt-3.5-turbo"
    }


# Mount static files directory
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
