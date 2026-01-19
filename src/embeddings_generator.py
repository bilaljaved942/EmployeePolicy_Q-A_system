"""Embeddings generation module for creating vector representations"""
from typing import List, Dict
import numpy as np
from .config import EMBEDDING_MODEL, USE_OPENAI_EMBEDDINGS, OPENAI_API_KEY


class EmbeddingsGenerator:
    """Generates embeddings for text chunks"""
    
    def __init__(self):
        self.use_openai = USE_OPENAI_EMBEDDINGS
        self.model_name = EMBEDDING_MODEL
        
        if self.use_openai:
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            from openai import OpenAI
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            print("Using OpenAI embeddings")
        else:
            from sentence_transformers import SentenceTransformer
            print(f"Loading local embedding model: {self.model_name}")
            self.embedding_model = SentenceTransformer(self.model_name)
            print("Model loaded successfully")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if self.use_openai:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        else:
            return self.embedding_model.encode(text, convert_to_numpy=True).tolist()
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings for multiple texts in batches"""
        if self.use_openai:
            # OpenAI handles batching internally
            embeddings = []
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = self.client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=batch
                )
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
            return embeddings
        else:
            # Use sentence transformers batch processing
            embeddings = self.embedding_model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=True,
                convert_to_numpy=True
            )
            return embeddings.tolist()
    
    def add_embeddings_to_chunks(self, chunks: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Add embeddings to chunked documents"""
        texts = [chunk["content"] for chunk in chunks]
        
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.generate_embeddings_batch(texts)
        
        # Add embeddings to chunks
        for i, chunk in enumerate(chunks):
            chunk["embedding"] = embeddings[i]
        
        print(f"Successfully generated embeddings for {len(chunks)} chunks")
        return chunks
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        if self.use_openai:
            return 1536  # OpenAI ada-002 dimension
        else:
            # Test with a small text to get dimension
            test_embedding = self.generate_embedding("test")
            return len(test_embedding)


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.document_processor import DocumentProcessor
    from src.text_chunker import TextChunker
    
    # Process and chunk documents
    processor = DocumentProcessor()
    documents = processor.process_all_documents()
    
    chunker = TextChunker()
    chunks = chunker.chunk_all_documents(documents)
    
    # Generate embeddings
    print("\n" + "="*60)
    print("Generating Embeddings")
    print("="*60)
    
    try:
        embeddings_gen = EmbeddingsGenerator()
        dimension = embeddings_gen.get_embedding_dimension()
        print(f"Embedding dimension: {dimension}")
        
        chunks_with_embeddings = embeddings_gen.add_embeddings_to_chunks(chunks)
        
        print(f"\nSample embedding (first 10 dimensions):")
        if chunks_with_embeddings:
            sample_embedding = chunks_with_embeddings[0]["embedding"]
            print(sample_embedding[:10])
    except Exception as e:
        print(f"Error: {e}")
        print("Note: For OpenAI embeddings, set OPENAI_API_KEY in .env file")
