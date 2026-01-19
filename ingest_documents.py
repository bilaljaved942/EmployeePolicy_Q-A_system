"""Script to ingest documents into the vector database"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_pipeline import RAGPipeline


def main():
    """Run document ingestion"""
    print("="*60)
    print("Document Ingestion Pipeline")
    print("="*60)
    
    pipeline = RAGPipeline()
    summary = pipeline.ingest_documents()
    
    print("\n" + "="*60)
    print("Ingestion completed successfully!")
    print("="*60)
    print(f"Documents processed: {summary['documents_processed']}")
    print(f"Total chunks created: {summary['total_chunks']}")
    print(f"Embedding dimension: {summary['embedding_dimension']}")
    print(f"Vector store type: {summary['vector_store']['type']}")
    print(f"Documents in store: {summary['vector_store']['document_count']}")


if __name__ == "__main__":
    main()
