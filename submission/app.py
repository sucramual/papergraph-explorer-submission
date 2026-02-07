#!/usr/bin/env python3
"""
FastAPI backend for PaperGraph Explorer.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configure cognee
os.environ["VECTOR_DB_PROVIDER"] = "qdrant"
os.environ["VECTOR_DB_URL"] = os.getenv("QDRANT_URL", "http://localhost:6333")
os.environ["VECTOR_DB_KEY"] = os.getenv("QDRANT_API_KEY", "")

os.environ["LLM_PROVIDER"] = "openai"
os.environ["LLM_MODEL"] = "gpt-4o-mini"
os.environ["LLM_API_KEY"] = os.getenv("OPENAI_API_KEY")

os.environ["EMBEDDING_PROVIDER"] = "ollama"
os.environ["EMBEDDING_MODEL"] = "nomic-embed-text:latest"
os.environ["EMBEDDING_ENDPOINT"] = "http://localhost:11434/api/embed"
os.environ["EMBEDDING_DIMENSIONS"] = "768"

import cognee_community_vector_adapter_qdrant.register
from custom_retriever import GraphCompletionRetrieverWithUserPrompt
import pathlib

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/api/graph")
async def get_graph():
    """
    Get graph data for visualization.
    Returns: {nodes: [...], edges: [...]}

    Uses fallback strategy: Build simple graph from papers_metadata.json
    where first 10 papers are "seed papers" and rest are "related papers".
    """
    try:
        # Load papers from JSON
        with open("papers_metadata.json") as f:
            all_papers = json.load(f)

        papers = all_papers  # Use all papers (match ingestion count)

        # Create nodes
        # First 20 papers = seed papers (highly relevant)
        # Rest = related papers
        seed_count = min(20, len(papers) // 10)
        nodes = []
        for i, paper in enumerate(papers):
            node = {
                "id": paper['id'],
                "label": paper['title'][:35] + "..." if len(paper['title']) > 35 else paper['title'],
                "title": paper['title'],  # Tooltip
                "color": "#4A90E2" if i < seed_count else "#7B8D93",  # Blue for seed, gray for related
                "size": 20 if i < seed_count else 10
            }
            nodes.append(node)

        # Create edges: seed papers connect to related papers
        # To avoid too many edges with 500 papers, connect each seed to ~10 related papers
        edges = []
        related_per_seed = min(10, (len(papers) - seed_count) // seed_count) if seed_count > 0 else 0
        for i in range(seed_count):
            for j in range(seed_count, min(seed_count + (i+1) * related_per_seed, len(papers))):
                edges.append({
                    "from": papers[i]['id'],
                    "to": papers[j]['id'],
                    "arrows": "to"
                })

        return {"nodes": nodes, "edges": edges}

    except Exception as e:
        print(f"Error loading graph: {e}")
        return {"nodes": [], "edges": []}

@app.get("/api/paper/{paper_id}")
async def get_paper(paper_id: str):
    """Get details for a specific paper."""
    try:
        with open("papers_metadata.json") as f:
            papers = json.load(f)

        for paper in papers:
            if paper['id'] == paper_id:
                return paper

        return {"error": "Paper not found"}
    except Exception as e:
        return {"error": str(e)}

class QueryRequest(BaseModel):
    paper_id: str
    question: str

@app.post("/api/query")
async def query_paper(req: QueryRequest):
    """
    Answer question about a selected paper.
    """
    try:
        # Use custom retriever to get graph context + OpenAI
        system_prompt_path = pathlib.Path("prompts/system_prompt.txt").resolve()

        retriever = GraphCompletionRetrieverWithUserPrompt(
            user_prompt_filename="user_prompt.txt",
            system_prompt_path=str(system_prompt_path),
            top_k=10,
        )

        # Build query with paper context
        query = f"Paper ID: {req.paper_id}\nQuestion: {req.question}"

        completion = await retriever.get_completion(query=query)

        return {"answer": completion[0]}

    except Exception as e:
        print(f"Error in query: {e}")
        return {"answer": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    print("Starting PaperGraph Explorer on http://localhost:7777")
    print("Open your browser to view the interactive graph")
    uvicorn.run(app, host="0.0.0.0", port=7777)
