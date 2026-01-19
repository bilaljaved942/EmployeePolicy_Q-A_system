"""Main entry point for the Employee Policy Q&A System"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_pipeline import RAGPipeline
from src.qa_system import QASystem


def main():
    """Main function to run the Q&A system"""
    print("="*60)
    print("Employee Policy Q&A System")
    print("="*60)
    
    # Initialize pipeline
    print("\nInitializing RAG pipeline...")
    pipeline = RAGPipeline()
    
    # Check if documents are ingested
    store_info = pipeline.vector_store.get_collection_info()
    if store_info.get("document_count", 0) == 0:
        print("\nNo documents found in vector store. Running ingestion...")
        pipeline.ingest_documents()
    else:
        print(f"\nFound {store_info['document_count']} documents in vector store.")
    
    # Initialize Q&A system
    print("\nInitializing Q&A System...")
    qa = QASystem(pipeline)
    
    # Interactive Q&A
    print("\n" + "="*60)
    print("Ready for questions!")
    print("Type your questions about employee policies.")
    print("Type 'quit' or 'exit' to end the session.")
    print("="*60 + "\n")
    
    while True:
        try:
            question = input("Question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the Employee Policy Q&A System. Goodbye!")
                break
            
            if not question:
                continue
            
            print("\nSearching for answer...")
            result = qa.answer(question)
            
            print(f"\n{'='*60}")
            print("Answer:")
            print(f"{'='*60}")
            print(result['answer'])
            print(f"\n{'='*60}")
            print("Sources:")
            for i, source in enumerate(result['sources'], 1):
                print(f"  {i}. {source['source']} (relevance: {source['relevance_score']:.2f})")
            print("="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the Employee Policy Q&A System. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
