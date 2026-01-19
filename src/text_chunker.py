"""Text chunking module for splitting documents into manageable chunks"""
from typing import List, Dict
import re
from .config import CHUNK_SIZE, CHUNK_OVERLAP


class TextChunker:
    """Handles text chunking with overlap for better context preservation"""
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def _split_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        separators = ["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        
        start = 0
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            if end >= len(text):
                # Last chunk
                chunks.append(text[start:])
                break
            
            # Try to find a good break point
            best_break = end
            for sep in separators:
                # Look for separator before end
                for i in range(end, max(start, end - 200), -1):
                    if text[i:i+len(sep)] == sep:
                        best_break = i + len(sep)
                        break
                if best_break < end:
                    break
            
            chunk = text[start:best_break].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = max(start + 1, best_break - self.chunk_overlap)
        
        return chunks
    
    def chunk_document(self, document: Dict[str, str]) -> List[Dict[str, str]]:
        """Split a document into chunks with metadata"""
        text = document["content"]
        chunks = self._split_text(text)
        
        chunked_documents = []
        for i, chunk in enumerate(chunks):
            chunk_doc = {
                "chunk_id": f"{document['filename']}_chunk_{i}",
                "content": chunk,
                "metadata": {
                    **document["metadata"],
                    "source": document["filename"],
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "chunk_size": len(chunk)
                }
            }
            chunked_documents.append(chunk_doc)
        
        return chunked_documents
    
    def chunk_all_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Chunk all documents"""
        all_chunks = []
        
        for document in documents:
            chunks = self.chunk_document(document)
            all_chunks.extend(chunks)
            print(f"  Created {len(chunks)} chunks from {document['filename']}")
        
        return all_chunks
    
    def get_chunking_statistics(self, chunks: List[Dict[str, str]]) -> Dict:
        """Get statistics about chunking"""
        if not chunks:
            return {}
        
        chunk_sizes = [len(chunk["content"]) for chunk in chunks]
        total_chars = sum(chunk_sizes)
        
        return {
            "total_chunks": len(chunks),
            "total_characters": total_chars,
            "average_chunk_size": total_chars / len(chunks) if chunks else 0,
            "min_chunk_size": min(chunk_sizes) if chunk_sizes else 0,
            "max_chunk_size": max(chunk_sizes) if chunk_sizes else 0
        }


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.document_processor import DocumentProcessor
    
    # Process documents
    processor = DocumentProcessor()
    documents = processor.process_all_documents()
    
    # Chunk documents
    chunker = TextChunker()
    chunks = chunker.chunk_all_documents(documents)
    
    print("\n" + "="*60)
    print("Chunking Summary")
    print("="*60)
    stats = chunker.get_chunking_statistics(chunks)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print(f"\nSample chunk (first 200 characters):")
    if chunks:
        print(chunks[0]["content"][:200] + "...")
