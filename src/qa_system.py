"""Q&A System that uses RAG to answer questions about employee policies"""
from typing import List, Dict, Optional
from .rag_pipeline import RAGPipeline
from .config import LLM_MODEL, USE_LOCAL_LLM, OPENAI_API_KEY, TOP_K_RESULTS, MAX_TOKENS, TEMPERATURE


class QASystem:
    """Question-Answering system using RAG"""
    
    def __init__(self, pipeline: Optional[RAGPipeline] = None):
        self.pipeline = pipeline or RAGPipeline()
        self.llm_model = LLM_MODEL
        self.use_local_llm = USE_LOCAL_LLM
        
        if not self.use_local_llm:
            if not OPENAI_API_KEY:
                print("Warning: OPENAI_API_KEY not found. LLM features will be limited.")
                self.llm_client = None
            else:
                from openai import OpenAI
                self.llm_client = OpenAI(api_key=OPENAI_API_KEY)
        else:
            # For local LLM, you would initialize here
            self.llm_client = None
            print("Local LLM mode (not implemented yet)")
    
    def _format_context(self, search_results: List[Dict]) -> str:
        """Format search results into context for the LLM"""
        context_parts = []
        for i, result in enumerate(search_results, 1):
            source = result['metadata'].get('source', 'Unknown')
            content = result['content']
            context_parts.append(f"[Document {i} - Source: {source}]\n{content}\n")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, question: str, context: str) -> str:
        """Create a prompt for the LLM"""
        prompt = f"""You are a helpful assistant that answers questions about employee policies and HR procedures for XCorp Technologies Private Limited.

Use the following context from company documents to answer the question. If the answer is not in the context, say so.

Context:
{context}

Question: {question}

Answer:"""
        return prompt
    
    def answer(self, question: str, use_llm: bool = True) -> Dict[str, any]:
        """Answer a question using RAG"""
        # Step 1: Retrieve relevant documents
        search_results = self.pipeline.search(question, top_k=TOP_K_RESULTS)
        
        if not search_results:
            return {
                "question": question,
                "answer": "I couldn't find relevant information in the company documents to answer this question.",
                "sources": [],
                "confidence": 0.0
            }
        
        # Step 2: Format context
        context = self._format_context(search_results)
        
        # Step 3: Generate answer
        if use_llm and self.llm_client:
            try:
                prompt = self._create_prompt(question, context)
                
                response = self.llm_client.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions about employee policies based on provided documents."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE
                )
                
                answer = response.choices[0].message.content
            except Exception as e:
                print(f"Error calling LLM: {e}")
                answer = self._extract_answer_from_context(question, context)
        else:
            # Fallback: extract relevant text from context
            answer = self._extract_answer_from_context(question, context)
        
        # Step 4: Prepare sources
        sources = [
            {
                "source": result['metadata'].get('source', 'Unknown'),
                "chunk_id": result.get('chunk_id', ''),
                "relevance_score": 1.0 - (result.get('distance', 0) / 10) if result.get('distance') else 1.0
            }
            for result in search_results
        ]
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "confidence": sources[0]['relevance_score'] if sources else 0.0
        }
    
    def _extract_answer_from_context(self, question: str, context: str) -> str:
        """Extract answer from context when LLM is not available"""
        # Simple extraction: return the most relevant chunk
        # In a real implementation, you might use better extraction methods
        lines = context.split('\n')
        relevant_lines = []
        
        question_lower = question.lower()
        question_words = set(question_lower.split())
        
        for line in lines:
            line_lower = line.lower()
            # Count matching words
            matches = sum(1 for word in question_words if word in line_lower)
            if matches > 0:
                relevant_lines.append(line)
        
        if relevant_lines:
            return "\n".join(relevant_lines[:5])  # Return top 5 relevant lines
        else:
            return context[:500]  # Return first 500 chars as fallback
    
    def chat(self, question: str) -> str:
        """Simple chat interface"""
        result = self.answer(question)
        return result["answer"]


if __name__ == "__main__":
    import sys
    
    # Initialize Q&A system
    print("Initializing Q&A System...")
    qa = QASystem()
    
    # Check if documents are ingested
    store_info = qa.pipeline.vector_store.get_collection_info()
    if store_info.get("document_count", 0) == 0:
        print("\nNo documents found in vector store. Running ingestion...")
        qa.pipeline.ingest_documents()
    
    # Interactive Q&A
    print("\n" + "="*60)
    print("Employee Policy Q&A System")
    print("="*60)
    print("Type your questions about employee policies.")
    print("Type 'quit' or 'exit' to end the session.\n")
    
    while True:
        try:
            question = input("Question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not question:
                continue
            
            print("\nSearching for answer...")
            result = qa.answer(question)
            
            print(f"\nAnswer: {result['answer']}")
            print(f"\nSources:")
            for i, source in enumerate(result['sources'], 1):
                print(f"  {i}. {source['source']} (relevance: {source['relevance_score']:.2f})")
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
