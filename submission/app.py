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

        papers = all_papers[:50]  # Show 50 papers for clean visualization

        # Create nodes with three-tier system:
        # Tier 1: "Attention Is All You Need" (1 paper) - Orange, largest
        # Tier 2: Seed papers (15 papers) - Blue, medium
        # Tier 3: Related papers (34 papers) - Gray, small
        seed_count = 15
        nodes = []
        for i, paper in enumerate(papers):
            # Highlight "Attention Is All You Need" paper (arXiv ID: 1706.03762)
            is_attention_paper = paper['id'] == '1706.03762'

            node = {
                "id": paper['id'],
                "label": paper['title'][:40] + "..." if len(paper['title']) > 40 else paper['title'],
                "title": paper['title'],  # Tooltip
                # Three-tier color system
                "color": "#FF6B35" if is_attention_paper else ("#4A90E2" if i < seed_count else "#95A5A6"),
                # Three-tier size system
                "size": 35 if is_attention_paper else (25 if i < seed_count else 15),
                # Border styling
                "borderWidth": 4 if is_attention_paper else (2 if i < seed_count else 1),
                "borderColor": "#FF6B35" if is_attention_paper else ("#2E86C1" if i < seed_count else "#7F8C8D")
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

@app.get("/api/paper/{paper_id}/related")
async def get_related_papers(paper_id: str):
    """Get papers related to a specific paper based on graph connections."""
    try:
        # Load all papers
        with open("papers_metadata.json") as f:
            all_papers = json.load(f)

        # Get graph data to find connections
        graph_data = await get_graph()

        # Find papers connected to this one
        related_ids = set()
        for edge in graph_data["edges"]:
            if edge["from"] == paper_id:
                related_ids.add(edge["to"])
            elif edge["to"] == paper_id:
                related_ids.add(edge["from"])

        # Get details for related papers
        related_papers = []
        papers_dict = {p['id']: p for p in all_papers}

        for rel_id in related_ids:
            if rel_id in papers_dict:
                paper = papers_dict[rel_id]
                related_papers.append({
                    "id": paper['id'],
                    "title": paper['title'],
                    "authors": paper['authors'][:3],  # First 3 authors
                    "published": paper['published']
                })

        return {"related_papers": related_papers, "count": len(related_papers)}
    except Exception as e:
        return {"error": str(e), "related_papers": [], "count": 0}

class QueryRequest(BaseModel):
    paper_id: str
    question: str

@app.post("/api/query")
async def query_paper(req: QueryRequest):
    """
    Answer question about a selected paper using Qdrant vector search.
    Uses cognee's GraphCompletionRetriever to search Qdrant and retrieve relevant context.
    """
    try:
        # Load the specific paper from metadata
        with open("papers_metadata.json") as f:
            all_papers = json.load(f)

        target_paper = None
        for paper in all_papers:
            if paper['id'] == req.paper_id:
                target_paper = paper
                break

        if not target_paper:
            return {"answer": "Paper not found in database."}

        # Use GraphCompletionRetriever to search Qdrant vector database
        system_prompt_path = pathlib.Path("prompts/system_prompt.txt").resolve()

        retriever = GraphCompletionRetrieverWithUserPrompt(
            user_prompt_filename="user_prompt.txt",
            system_prompt_path=str(system_prompt_path),
            top_k=10,  # Retrieve top 10 most relevant vectors from Qdrant
        )

        # Build query with paper context
        query = f"""
Paper: {target_paper['title']}
Authors: {', '.join(target_paper['authors'])}

Question: {req.question}
"""

        # This uses Qdrant vector search to find relevant context
        # Then uses OpenAI with that context to generate answer
        completion = await retriever.get_completion(query=query)

        return {
            "answer": completion[0],
            "method": "qdrant_vector_search"  # Flag showing we used Qdrant
        }

    except Exception as e:
        print(f"Error in query (falling back to simple approach): {e}")
        import traceback
        traceback.print_exc()

        # Fallback: Use OpenAI directly if Qdrant retrieval fails
        try:
            paper_context = f"""
Paper: {target_paper['title']}
Authors: {', '.join(target_paper['authors'])}
Abstract: {target_paper['summary']}
"""
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an academic research assistant."},
                    {"role": "user", "content": f"{paper_context}\n\nQuestion: {req.question}"}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return {
                "answer": response.choices[0].message.content,
                "method": "fallback_direct"
            }
        except Exception as e2:
            return {"answer": f"Error: {str(e2)}", "method": "error"}

if __name__ == "__main__":
    import uvicorn
    print("Starting PaperGraph Explorer on http://localhost:7777")
    print("Open your browser to view the interactive graph")
    uvicorn.run(app, host="0.0.0.0", port=7777)
