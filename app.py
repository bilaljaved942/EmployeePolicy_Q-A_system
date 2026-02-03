"""FastAPI application for Employee Policy Q&A System with Multi-User Support"""
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os
import uuid
import json
from datetime import datetime, timedelta
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_pipeline import RAGPipeline
from src.qa_system import QASystem
from src.models import User, Document, ChatHistory, init_db, get_db
from src.auth import (
    get_current_user, create_user, authenticate_user, 
    create_access_token, get_user_by_email, get_user_by_username,
    get_password_hash, Token, TokenData
)
from src.schemas import (
    UserRegister, UserLogin, UserResponse, DocumentResponse,
    QuestionRequest, AnswerResponse, SourceInfo, ChatHistoryResponse,
    ChatMessage, StatsResponse
)

# Initialize FastAPI app
app = FastAPI(
    title="Employee Policy Q&A System",
    description="RAG-based Q&A system with multi-user support",
    version="2.0.0"
)

# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache control middleware to prevent caching of API responses
@app.middleware("http")
async def add_cache_control(request, call_next):
    """Add cache control headers to prevent stale data"""
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized!")

# Create uploads directory
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ===== AUTHENTICATION ENDPOINTS =====

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    new_user = create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )
    
    return new_user


@app.post("/api/auth/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    user = authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    token_data = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }
    access_token = create_access_token(token_data)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username
    )


@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


# ===== DOCUMENT UPLOAD ENDPOINTS =====

@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Save file
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        user_upload_dir = os.path.join(UPLOAD_DIR, f"user_{current_user.id}")
        os.makedirs(user_upload_dir, exist_ok=True)
        
        file_path = os.path.join(user_upload_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = os.path.getsize(file_path)
        
        # Create document record
        doc = Document(
            user_id=current_user.id,
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            document_type="user_upload"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        # Process document asynchronously would be better, but for now we'll do it synchronously
        try:
            pipeline = RAGPipeline(user_id=current_user.id)
            result = pipeline.ingest_single_document(file_path, file.filename)
            
            doc.is_processed = True
            doc.processed_at = datetime.utcnow()
            doc.chunk_count = result.get("chunks_created", 0)
            doc.vector_collection_name = f"user_{current_user.id}_documents"
            db.commit()
        except Exception as e:
            doc.is_processed = False
            db.commit()
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
        
        return doc
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")


@app.get("/api/documents", response_model=List[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents for the current user"""
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents


@app.delete("/api/documents/{doc_id}")
async def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document"""
    doc = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)
    
    # Delete from database
    db.delete(doc)
    db.commit()
    
    return {"message": "Document deleted successfully"}


# ===== CHAT ENDPOINTS =====

@app.post("/api/ask", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ask a question and get an answer with STRICT user isolation"""
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # STRICT USER ISOLATION: Initialize user-specific pipeline with current_user.id
        # This ensures all documents searched belong only to this user
        pipeline = RAGPipeline(user_id=current_user.id)
        qa_system = QASystem(pipeline)
        
        # Get answer (with strict isolation validation)
        result = qa_system.answer(request.question.strip())
        
        # Save to chat history with user_id
        session_id = request.session_id or str(uuid.uuid4())
        sources_json = json.dumps([
            {"source": s["source"], "relevance_score": s["relevance_score"]}
            for s in result["sources"]
        ])
        
        chat = ChatHistory(
            user_id=current_user.id,
            session_id=session_id,
            question=request.question,
            answer=result["answer"],
            confidence_score=result["confidence"],
            sources=sources_json
        )
        db.add(chat)
        db.commit()
        
        # Format response
        sources = [
            SourceInfo(
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
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.get("/api/chat-history", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history for the current user"""
    query = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id)
    
    if session_id:
        query = query.filter(ChatHistory.session_id == session_id)
    
    messages = query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
    
    return ChatHistoryResponse(
        messages=list(reversed(messages)),
        total=len(messages)
    )


# ===== STATS ENDPOINTS =====

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system statistics for the current user"""
    user_docs = db.query(Document).filter(Document.user_id == current_user.id).count()
    
    pipeline = RAGPipeline(user_id=current_user.id)
    store_info = pipeline.vector_store.get_collection_info()
    
    return StatsResponse(
        user_documents_count=user_docs,
        total_chunks=store_info.get("document_count", 0),
        user_id=current_user.id,
        username=current_user.username
    )


# ===== HEALTH CHECK =====

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0"
    }


# ===== SERVE FRONTEND =====

@app.get("/favicon.svg")
async def favicon():
    """Serve favicon"""
    favicon_path = os.path.join("static", "favicon.svg")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/svg+xml")
    raise HTTPException(status_code=404, detail="Favicon not found")

@app.get("/favicon.ico")
async def favicon_ico():
    """Serve favicon.ico (fallback)"""
    favicon_path = os.path.join("static", "favicon.svg")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/svg+xml")
    raise HTTPException(status_code=404, detail="Favicon not found")

@app.get("/")
async def read_root():
    """Serve the frontend HTML file"""
    return FileResponse("static/index.html")


# Mount static files directory
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
