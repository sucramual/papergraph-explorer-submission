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

import cognee_community_vector_adapter_qdrant.register
import cognee
import asyncio
import sys
from tqdm.asyncio import tqdm

async def main():
    # Load papers metadata with error handling
    try:
        with open("papers_metadata.json") as f:
            all_papers = json.load(f)
        assert all_papers, "papers_metadata.json is empty"
    except FileNotFoundError:
        print("❌ papers_metadata.json not found. Run parse_metadata.py first.\n", flush=True)
        sys.exit(1)
    except (json.JSONDecodeError, AssertionError) as e:
        print(f"❌ Error loading papers: {e}\n", flush=True)
        sys.exit(1)

    # Clear old data
    print("Clearing old cognee data...", flush=True)
    await cognee.prune.prune_data()
    print("✓ Old data cleared\n", flush=True)

    # Select papers for ingestion
    papers = all_papers[:100]
    print(f"Ingesting {len(papers)} papers...\n", flush=True)

    # Add each paper to cognee with progress bar
    progress_bar = tqdm(papers, desc="📄 Adding papers", unit="paper")

    for paper in progress_bar:
        text = f"""
Paper: {paper['title']}
Authors: {', '.join(paper['authors'])}
arXiv ID: {paper['id']}
Published: {paper['published']}

Abstract:
{paper['summary']}
"""
        await cognee.add(text, dataset_name="papers")

        # Update progress bar description with current paper
        progress_bar.set_postfix_str(paper['title'][:50] + "...")

    # Build knowledge graph
    print(f"\n✓ All {len(papers)} papers added", flush=True)
    est_time = "~30 seconds" if len(papers) <= 10 else f"~{len(papers)//2} minutes"
    print(f"\nBuilding knowledge graph (estimated time: {est_time})...", flush=True)
    await cognee.cognify()

    print("\n" + "="*60, flush=True)
    print("✓ Graph built successfully!", flush=True)
    print("="*60, flush=True)
    print("\nNext step: Run 'python3 app.py' to start the server", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
