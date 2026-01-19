"""Configuration file for the RAG system"""
import os
from dotenv import load_dotenv

load_dotenv()

# PDF Documents Configuration
PDF_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "documents")
PDF_FILES = [
    "Employment_Contract_XCorp.pdf",
    "HR_Policy_Handbook_XCorp.pdf",
    "Increment_and_Probation_Policy_XCorp.pdf"
]

# Chunking Configuration
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks

# Embedding Configuration
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI model
USE_OPENAI_EMBEDDINGS = True  # Using OpenAI embeddings for better quality

# Vector Database Configuration
VECTOR_DB_TYPE = "chroma"  # Options: "chroma", "faiss"
VECTOR_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_db")
COLLECTION_NAME = "employee_policies"

# LLM Configuration (for Q&A)
LLM_MODEL = "gpt-3.5-turbo"  # OpenAI model
USE_LOCAL_LLM = False  # Using OpenAI LLM

# API Keys (set in .env file)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Retrieval Configuration
TOP_K_RESULTS = 3  # Number of relevant chunks to retrieve
SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score for retrieval

# Q&A Configuration
MAX_TOKENS = 500
TEMPERATURE = 0.7
