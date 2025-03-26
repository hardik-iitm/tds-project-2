import asyncio
from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from typing import List
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for all origins (you can customize as needed)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow these methods
    allow_headers=["*"],
)

# Set your OpenAI API key
OPENAI_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDIyOTFAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.DuTpd4IaEMZT5E5c2ZZgt7s2bhrpn5VOurdBiwZLK4s'
# Define the input model for the POST request
class SimilarityRequest(BaseModel):
    docs: List[str]
    query: str

# Helper function to compute embeddings using OpenAI's API via httpx
async def embed(text: str) -> list[float]:
    """Get embedding vector for text using OpenAI's API."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/embeddings",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={"model": "text-embedding-3-small", "input": text}
        )
        
        # Check if the response was successful (status code 200)
        if response.status_code == 200:
            embedding = response.json()  # Assuming the response contains JSON with the embeddings
            print("Embedding:", embedding)
            return embedding['data'][0]['embedding']  # Assuming the response contains the embedding in this format
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

# Cosine similarity calculation
def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# POST endpoint for similarity search
@app.post("/similarity")
async def similarity(request: SimilarityRequest):
    try:
        # Combine docs and query to calculate embeddings
        docs = request.docs
        query = request.query
        
        # Compute embeddings for docs and the query (await the async function)
        all_texts = docs + [query]
        embeddings = []
        for text in all_texts:
            embedding = await embed(text)  # Await each embedding request
            embeddings.append(embedding)
        # Split embeddings into document embeddings and query embedding
        doc_embeddings = embeddings[:-1]
        query_embedding = embeddings[-1]
        print(query_embedding)
        # Calculate cosine similarities between the query and each document
        similarities = []
        for doc_embedding in doc_embeddings:
            similarity_score = cosine_similarity(np.array(doc_embedding), np.array(query_embedding))
            similarities.append(similarity_score)
        
        # Rank documents by similarity (highest first)
        ranked_indices = np.argsort(similarities)[::-1]  # Sort descending
        matches = [docs[i] for i in ranked_indices[:3]]  # Get top 3 matches
        
        # Return the top 3 matching documents
        return {"matches": matches}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))