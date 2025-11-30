"""
Vector database operations using ChromaDB
"""
import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import hashlib


class VectorStore:
    """ChromaDB vector store for resumes and job descriptions"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB client"""
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collections
        self.resume_collection = self.client.get_or_create_collection(
            name="resumes",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.job_collection = self.client.get_or_create_collection(
            name="job_descriptions",
            metadata={"hnsw:space": "cosine"}
        )
    
    def _generate_id(self, text: str) -> str:
        """Generate unique ID from text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _embed_text(self, text: str) -> List[float]:
        """Generate embedding for text"""
        embedding = self.embedding_model.encode(text).tolist()
        return embedding
    
    def add_resume(self, resume_text: str, metadata: Dict) -> str:
        """Add resume to vector store"""
        resume_id = self._generate_id(resume_text)
        
        # Check if already exists
        existing = self.resume_collection.get(ids=[resume_id])
        if existing['ids']:
            return resume_id
        
        embedding = self._embed_text(resume_text)
        
        # Clean metadata - only keep simple types
        clean_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool, type(None))):
                clean_metadata[key] = value
            else:
                # Skip complex types or convert to string representation
                if isinstance(value, dict):
                    clean_metadata[f"{key}_keys"] = str(list(value.keys())[:5])  # Store first 5 keys
                elif isinstance(value, list):
                    clean_metadata[f"{key}_count"] = len(value)
        
        self.resume_collection.add(
            embeddings=[embedding],
            documents=[resume_text],
            ids=[resume_id],
            metadatas=[clean_metadata]
        )
        
        return resume_id
    
    def add_job_description(self, job_text: str, metadata: Dict) -> str:
        """Add job description to vector store"""
        job_id = self._generate_id(job_text)
        
        embedding = self._embed_text(job_text)
        
        # Clean metadata - only keep simple types
        clean_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool, type(None))):
                clean_metadata[key] = value
            else:
                # Skip complex types or convert to string representation
                if isinstance(value, dict):
                    clean_metadata[f"{key}_keys"] = str(list(value.keys())[:5])  # Store first 5 keys
                elif isinstance(value, list):
                    clean_metadata[f"{key}_count"] = len(value)
        
        self.job_collection.add(
            embeddings=[embedding],
            documents=[job_text],
            ids=[job_id],
            metadatas=[clean_metadata]
        )
        
        return job_id
    
    def search_similar_resumes(self, job_description: str, top_k: int = 10) -> List[Dict]:
        """Search for similar resumes based on job description"""
        query_embedding = self._embed_text(job_description)
        
        results = self.resume_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts"""
        embedding1 = self._embed_text(text1)
        embedding2 = self._embed_text(text2)
        
        # Calculate cosine similarity
        import numpy as np
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    
    def clear_collections(self):
        """Clear all collections"""
        try:
            self.client.delete_collection(name="resumes")
            self.client.delete_collection(name="job_descriptions")
        except:
            pass
        
        # Recreate collections
        self.resume_collection = self.client.get_or_create_collection(
            name="resumes",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.job_collection = self.client.get_or_create_collection(
            name="job_descriptions",
            metadata={"hnsw:space": "cosine"}
        )

