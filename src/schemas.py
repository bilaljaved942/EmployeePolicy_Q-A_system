"""Pydantic models for request/response validation"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ===== Authentication Schemas =====
class UserRegister(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)  # Bcrypt max length is 72
    full_name: Optional[str] = Field(None, max_length=100)


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response (without password)"""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Document Schemas =====
class DocumentResponse(BaseModel):
    """Document response"""
    id: int
    filename: str
    original_filename: str
    file_size: Optional[int]
    document_type: Optional[str]
    chunk_count: int
    is_processed: bool
    created_at: datetime
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """List of documents"""
    documents: List[DocumentResponse]
    total: int


# ===== Chat Schemas =====
class SourceInfo(BaseModel):
    """Source information for an answer"""
    source: str
    relevance_score: float


class QuestionRequest(BaseModel):
    """Question request"""
    question: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[str] = None


class AnswerResponse(BaseModel):
    """Answer response"""
    question: str
    answer: str
    sources: List[SourceInfo]
    confidence: float


class ChatMessage(BaseModel):
    """Chat message for history"""
    id: int
    question: str
    answer: str
    confidence_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Chat history response"""
    messages: List[ChatMessage]
    total: int


# ===== System Schemas =====
class StatsResponse(BaseModel):
    """System statistics"""
    user_documents_count: int
    total_chunks: int
    user_id: int
    username: str
