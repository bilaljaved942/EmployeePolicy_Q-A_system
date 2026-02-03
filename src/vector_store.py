"""Vector database module for storing and retrieving embeddings"""
import os
from typing import List, Dict, Optional
from .config import VECTOR_DB_TYPE, VECTOR_DB_PATH, COLLECTION_NAME


class VectorStore:
    """Manages vector database operations with multi-tenant support"""
    
    def __init__(self, db_type: str = VECTOR_DB_TYPE, db_path: str = VECTOR_DB_PATH, user_id: int = None):
        self.db_type = db_type.lower()
        self.db_path = db_path
        self.user_id = user_id
        
        # Use user-specific collection name if user_id is provided
        if user_id:
            self.collection_name = f"user_{user_id}_documents"
        else:
            self.collection_name = COLLECTION_NAME
        
        if self.db_type == "chroma":
            self._init_chroma()
        elif self.db_type == "faiss":
            self._init_faiss()
        else:
            raise ValueError(f"Unsupported vector DB type: {db_type}")
    
    def _init_chroma(self):
        """Initialize ChromaDB"""
        import chromadb
        from chromadb.config import Settings
        
        # Create directory if it doesn't exist
        os.makedirs(self.db_path, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            print(f"Loaded existing ChromaDB collection: {self.collection_name}")
        except:
            # Only create new collection if it's a user-specific collection
            # This prevents creating a default "employee_policies" collection
            if self.user_id or self.collection_name.startswith("user_"):
                self.collection = self.client.create_collection(name=self.collection_name)
                print(f"Created new ChromaDB collection: {self.collection_name}")
            else:
                # For non-user collections, only create if explicitly needed
                self.collection = self.client.create_collection(name=self.collection_name)
                print(f"Created new ChromaDB collection: {self.collection_name}")
    
    def _init_faiss(self):
        """Initialize FAISS"""
        import faiss
        import pickle
        
        self.faiss_index = None
        self.metadata_store = {}
        self.index_path = os.path.join(self.db_path, "faiss_index.bin")
        self.metadata_path = os.path.join(self.db_path, "metadata.pkl")
        
        # Load existing index if it exists
        if os.path.exists(self.index_path):
            self.faiss_index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata_store = pickle.load(f)
            print(f"Loaded existing FAISS index with {self.faiss_index.ntotal} vectors")
        else:
            print("FAISS index will be created when first documents are added")
    
    def add_documents(self, chunks: List[Dict[str, str]]):
        """Add documents with embeddings to the vector store"""
        if not chunks:
            print("No chunks to add")
            return
        
        if self.db_type == "chroma":
            self._add_to_chroma(chunks)
        elif self.db_type == "faiss":
            self._add_to_faiss(chunks)
    
    def _add_to_chroma(self, chunks: List[Dict[str, str]]):
        """Add documents to ChromaDB"""
        ids = [chunk["chunk_id"] for chunk in chunks]
        texts = [chunk["content"] for chunk in chunks]
        embeddings = [chunk["embedding"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        
        print(f"Added {len(chunks)} documents to ChromaDB")
    
    def _add_to_faiss(self, chunks: List[Dict[str, str]]):
        """Add documents to FAISS"""
        import faiss
        import numpy as np
        import pickle
        
        embeddings = np.array([chunk["embedding"] for chunk in chunks], dtype='float32')
        
        # Get embedding dimension
        dimension = embeddings.shape[1]
        
        # Create index if it doesn't exist
        if self.faiss_index is None:
            # Use L2 distance (Euclidean)
            self.faiss_index = faiss.IndexFlatL2(dimension)
            print(f"Created FAISS index with dimension {dimension}")
        
        # Add embeddings to index
        self.faiss_index.add(embeddings)
        
        # Store metadata
        start_id = len(self.metadata_store)
        for i, chunk in enumerate(chunks):
            self.metadata_store[start_id + i] = {
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "metadata": chunk["metadata"]
            }
        
        # Save index and metadata
        os.makedirs(self.db_path, exist_ok=True)
        faiss.write_index(self.faiss_index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata_store, f)
        
        print(f"Added {len(chunks)} documents to FAISS. Total vectors: {self.faiss_index.ntotal}")
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        if self.db_type == "chroma":
            return self._search_chroma(query_embedding, top_k)
        elif self.db_type == "faiss":
            return self._search_faiss(query_embedding, top_k)
    
    def _search_chroma(self, query_embedding: List[float], top_k: int) -> List[Dict]:
        """Search in ChromaDB with STRICT user isolation"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 2  # Get more results to filter by user_id
        )
        
        # Format results and STRICTLY filter by user_id
        formatted_results = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                metadata = results['metadatas'][0][i]
                metadata_user_id = metadata.get('user_id')
                
                # STRICT: Must have user_id in metadata
                if metadata_user_id is None:
                    print(f"WARNING: Document {results['ids'][0][i]} has no user_id in metadata - SKIPPING")
                    continue
                
                # STRICT: MUST match the search user_id exactly
                if self.user_id:
                    if str(metadata_user_id) != str(self.user_id):
                        # Skip documents from other users
                        continue
                
                result = {
                    "chunk_id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": metadata,
                    "distance": results['distances'][0][i] if 'distances' in results else None
                }
                formatted_results.append(result)
                
                # Stop once we have enough results for this user
                if len(formatted_results) >= top_k:
                    break
        
        return formatted_results
    
    def _search_faiss(self, query_embedding: List[float], top_k: int) -> List[Dict]:
        """Search in FAISS with STRICT user isolation"""
        import numpy as np
        
        if self.faiss_index is None:
            return []
        
        query_vector = np.array([query_embedding], dtype='float32')
        
        # Search for more results to ensure we get enough after filtering
        search_k = min(top_k * 3, self.faiss_index.ntotal)
        distances, indices = self.faiss_index.search(query_vector, search_k)
        
        # Format results with STRICT user filtering
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata_store):
                metadata_entry = self.metadata_store[idx]
                metadata = metadata_entry["metadata"]
                metadata_user_id = metadata.get('user_id')
                
                # STRICT: Must have user_id in metadata
                if metadata_user_id is None:
                    print(f"WARNING: Document {metadata_entry['chunk_id']} has no user_id in metadata - SKIPPING")
                    continue
                
                # STRICT: MUST match the search user_id exactly
                if self.user_id:
                    if str(metadata_user_id) != str(self.user_id):
                        # Skip documents from other users
                        continue
                
                result = {
                    "chunk_id": metadata_entry["chunk_id"],
                    "content": metadata_entry["content"],
                    "metadata": metadata,
                    "distance": float(distances[0][i])
                }
                results.append(result)
                
                # Stop once we have enough results for this user
                if len(results) >= top_k:
                    break
        
        return results
    
    def get_collection_info(self) -> Dict:
        """Get information about the vector store"""
        if self.db_type == "chroma":
            count = self.collection.count()
            return {
                "type": "ChromaDB",
                "collection_name": self.collection_name,
                "document_count": count,
                "path": self.db_path,
                "user_id": self.user_id
            }
        elif self.db_type == "faiss":
            count = self.faiss_index.ntotal if self.faiss_index else 0
            return {
                "type": "FAISS",
                "document_count": count,
                "path": self.db_path,
                "user_id": self.user_id
            }
    
    def delete_collection(self):
        """Delete the current collection (for cleanup or user deletion)"""
        if self.db_type == "chroma":
            try:
                self.client.delete_collection(name=self.collection_name)
                print(f"Deleted ChromaDB collection: {self.collection_name}")
                return True
            except Exception as e:
                print(f"Error deleting collection: {e}")
                return False
        elif self.db_type == "faiss":
            import shutil
            try:
                if os.path.exists(self.index_path):
                    os.remove(self.index_path)
                if os.path.exists(self.metadata_path):
                    os.remove(self.metadata_path)
                print(f"Deleted FAISS index for user: {self.user_id}")
                return True
            except Exception as e:
                print(f"Error deleting FAISS index: {e}")
                return False


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.document_processor import DocumentProcessor
    from src.text_chunker import TextChunker
    from src.embeddings_generator import EmbeddingsGenerator
    
    # Process documents
    print("Processing documents...")
    processor = DocumentProcessor()
    documents = processor.process_all_documents()
    
    # Chunk documents
    print("\nChunking documents...")
    chunker = TextChunker()
    chunks = chunker.chunk_all_documents(documents)
    
    # Generate embeddings
    print("\nGenerating embeddings...")
    embeddings_gen = EmbeddingsGenerator()
    chunks_with_embeddings = embeddings_gen.add_embeddings_to_chunks(chunks)
    
    # Store in vector database
    print("\nStoring in vector database...")
    vector_store = VectorStore()
    vector_store.add_documents(chunks_with_embeddings)
    
    # Get info
    info = vector_store.get_collection_info()
    print("\n" + "="*60)
    print("Vector Store Information")
    print("="*60)
    for key, value in info.items():
        print(f"{key}: {value}")
