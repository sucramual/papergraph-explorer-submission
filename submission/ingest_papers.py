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

# Fix: Disable backend access control to avoid lancedb/qdrant mismatch
os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"

os.environ["LLM_PROVIDER"] = "openai"
os.environ["LLM_MODEL"] = "gpt-4o-mini"
os.environ["LLM_API_KEY"] = os.getenv("OPENAI_API_KEY")

os.environ["EMBEDDING_PROVIDER"] = "ollama"
os.environ["EMBEDDING_MODEL"] = "nomic-embed-text:latest"
os.environ["EMBEDDING_ENDPOINT"] = "http://localhost:11434/api/embed"
os.environ["EMBEDDING_DIMENSIONS"] = "768"
os.environ["HUGGINGFACE_TOKENIZER"] = "nomic-ai/nomic-embed-text-v1.5"

# Suppress HuggingFace warnings
os.environ["TRANSFORMERS_TRUST_REMOTE_CODE"] = "true"
if os.getenv("HF_TOKEN"):
    os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

import cognee_community_vector_adapter_qdrant.register
import cognee
import asyncio
import sys

async def main():
    # Clear old data (skip prune_system to avoid tokenizer issues during testing)
    print("Clearing old cognee data...", flush=True)
    await cognee.prune.prune_data()
    # Skip prune_system for now - causes tokenizer dependency issues
    # await cognee.prune.prune_system(metadata=True)
    print("✓ Old data cleared\n", flush=True)

    # Load papers metadata
    with open("papers_metadata.json") as f:
        all_papers = json.load(f)

    # Testing with 10 papers first
    papers = all_papers[:20]
    print(f"Ingesting {len(papers)} papers (testing mode)...\n", flush=True)

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
            print(f"Progress: {i}/{len(papers)} papers added", flush=True)
        elif i == 1 or i == len(papers):
            print(f"Added paper {i}: {paper['title'][:60]}...", flush=True)

    # Build knowledge graph
    print(f"\n✓ All {len(papers)} papers added", flush=True)
    print("\nBuilding knowledge graph (this may take 10-15 minutes)...", flush=True)
    await cognee.cognify()

    print("\n" + "="*60, flush=True)
    print("✓ Graph built successfully!", flush=True)
    print("="*60, flush=True)
    print("\nNext step: Run 'python3 app.py' to start the server", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
