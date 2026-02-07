#!/usr/bin/env python3
"""
Ingest papers into cognee and build knowledge graph.
"""
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configure cognee BEFORE importing
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
import cognee
import asyncio

async def main():
    # Clear old data
    print("Clearing old cognee data...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    print("✓ Old data cleared\n")

    # Load papers metadata
    with open("papers_metadata.json") as f:
        all_papers = json.load(f)

    # Use all papers (can change to [:50] for faster demo)
    papers = all_papers  # All 500 papers
    print(f"Ingesting {len(papers)} papers...\n")

    # Add each paper to cognee
    for i, paper in enumerate(papers, 1):
        text = f"""
Paper: {paper['title']}
Authors: {', '.join(paper['authors'])}
arXiv ID: {paper['id']}
Published: {paper['published']}

Abstract:
{paper['summary']}
"""
        await cognee.add(text, dataset_name="papers")

        if i % 10 == 0:
            print(f"Progress: {i}/{len(papers)} papers added")
        elif i == 1 or i == len(papers):
            print(f"Added paper {i}: {paper['title'][:60]}...")

    # Build knowledge graph
    print(f"\n✓ All {len(papers)} papers added")
    print("\nBuilding knowledge graph (this may take 10-15 minutes)...")
    await cognee.cognify()

    print("\n" + "="*60)
    print("✓ Graph built successfully!")
    print("="*60)
    print("\nNext step: Run 'python3 app.py' to start the server")

if __name__ == "__main__":
    asyncio.run(main())
