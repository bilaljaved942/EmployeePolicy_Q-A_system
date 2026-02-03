"""Main RAG pipeline that orchestrates document processing, chunking, embedding, and storage"""
from typing import List, Dict
import os
from .document_processor import DocumentProcessor
from .text_chunker import TextChunker
from .embeddings_generator import EmbeddingsGenerator
from .vector_store import VectorStore
from .config import PDF_FILES


class RAGPipeline:
    """Complete RAG pipeline for document ingestion with multi-tenant support"""
    
    def __init__(self, user_id: int = None):
        self.user_id = user_id
        self.processor = DocumentProcessor()
        self.chunker = TextChunker()
        self.embeddings_gen = EmbeddingsGenerator()
        self.vector_store = VectorStore(user_id=user_id)
    
    def ingest_documents(self) -> Dict:
        """Complete pipeline: extract, chunk, embed, and store documents"""
        print("="*60)
        print("RAG Pipeline - Document Ingestion")
        print("="*60)
        
        # Step 1: Process documents
        print("\n[Step 1/4] Processing PDF documents...")
        documents = self.processor.process_all_documents()
        if not documents:
            raise ValueError("No documents found to process")
        
        doc_stats = self.processor.get_document_statistics(documents)
        print(f"  Processed {doc_stats['total_documents']} documents")
        print(f"  Total characters: {doc_stats['total_characters']}")
        
        # Step 2: Chunk documents
        print("\n[Step 2/4] Chunking documents...")
        chunks = self.chunker.chunk_all_documents(documents)
        chunk_stats = self.chunker.get_chunking_statistics(chunks)
        print(f"  Created {chunk_stats['total_chunks']} chunks")
        print(f"  Average chunk size: {chunk_stats['average_chunk_size']:.0f} characters")
        
        # Step 3: Generate embeddings
        print("\n[Step 3/4] Generating embeddings...")
        chunks_with_embeddings = self.embeddings_gen.add_embeddings_to_chunks(chunks)
        embedding_dim = self.embeddings_gen.get_embedding_dimension()
        print(f"  Embedding dimension: {embedding_dim}")
        
        # Step 4: Store in vector database
        print("\n[Step 4/4] Storing in vector database...")
        self.vector_store.add_documents(chunks_with_embeddings)
        
        # Summary
        store_info = self.vector_store.get_collection_info()
        
        summary = {
            "documents_processed": doc_stats['total_documents'],
            "total_chunks": chunk_stats['total_chunks'],
            "embedding_dimension": embedding_dim,
            "vector_store": store_info
        }
        
        print("\n" + "="*60)
        print("Ingestion Complete!")
        print("="*60)
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        return summary
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant documents (STRICT user isolation)"""
        # STRICT: Must have a user_id
        if not self.user_id:
            raise ValueError("Cannot search without user_id - user isolation is required")
        
        # Check if user has any documents
        store_info = self.vector_store.get_collection_info()
        if store_info.get('document_count', 0) == 0:
            return []  # No documents for this user
        
        # Generate query embedding
        query_embedding = self.embeddings_gen.generate_embedding(query)
        
        # Search vector store (with STRICT user isolation)
        results = self.vector_store.search(query_embedding, top_k=top_k)
        
        # STRICT: Validate that ALL results belong to this user
        for result in results:
            result_user_id = result.get('metadata', {}).get('user_id')
            if str(result_user_id) != str(self.user_id):
                raise ValueError(
                    f"SECURITY ERROR: Search result contains document from user {result_user_id} "
                    f"but query is for user {self.user_id}. This should never happen!"
                )
        
        return results
    
    def ingest_single_document(self, file_path: str, original_filename: str) -> Dict:
        """Ingest a single document (for user uploads)"""
        print(f"Ingesting document: {original_filename}")
        
        # Step 1: Process the single document
        raw_text = self.processor.extract_text_from_pdf(file_path)
        cleaned_text = self.processor.clean_text(raw_text)
        
        document = {
            "filename": original_filename,
            "source": file_path,
            "content": cleaned_text,
            "metadata": {
                "document_type": self.processor._classify_document(original_filename),
                "file_size": os.path.getsize(file_path),
                "user_id": self.user_id
            }
        }
        
        # Step 2: Chunk the document
        chunks = self.chunker.chunk_document(document)
        print(f"  Created {len(chunks)} chunks")
        
        # Step 3: Generate embeddings
        chunks_with_embeddings = self.embeddings_gen.add_embeddings_to_chunks(chunks)
        
        # Step 4: Store in vector database
        self.vector_store.add_documents(chunks_with_embeddings)
        
        return {
            "filename": original_filename,
            "chunks_created": len(chunks),
            "characters": len(cleaned_text)
        }


if __name__ == "__main__":
    # Run the complete pipeline
    pipeline = RAGPipeline()
    summary = pipeline.ingest_documents()
    
    # Test search
    print("\n" + "="*60)
    print("Testing Search Functionality")
    print("="*60)
    
    test_queries = [
        "What is the probation period?",
        "How many annual leave days do employees get?",
        "What is the increment percentage after probation?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = pipeline.search(query, top_k=3)
        if results:
            print(f"Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"\n  Result {i}:")
                print(f"    Source: {result['metadata'].get('source', 'Unknown')}")
                print(f"    Content: {result['content'][:150]}...")
        else:
            print("  No results found")
