"""Test script for Q&A system"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_pipeline import RAGPipeline
from src.qa_system import QASystem


def test_questions():
    """Test the Q&A system with sample questions"""
    print("="*60)
    print("Testing Q&A System")
    print("="*60)
    
    # Initialize pipeline
    pipeline = RAGPipeline()
    
    # Initialize Q&A system
    qa = QASystem(pipeline)
    
    # Test questions
    test_questions = [
        "What is the probation period?",
        "How many annual leave days do employees get?",
        "What is the increment percentage after probation?",
        "What is the employee's name in the contract?",
        "Who is the Chief Human Resources Officer?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {question}")
        print("="*60)
        
        try:
            result = qa.answer(question)
            print(f"\nAnswer:\n{result['answer']}")
            print(f"\nSources:")
            for j, source in enumerate(result['sources'], 1):
                print(f"  {j}. {source['source']} (relevance: {source['relevance_score']:.2f})")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60)


if __name__ == "__main__":
    test_questions()
