# PaperGraph Explorer - Demo Script

**Project:** Interactive Knowledge Graph for Academic Papers with Natural Language Queries

**Time:** 5 minutes

---

## 🎯 The Problem

Academic researchers need to explore connections between papers, but:
- Reading 100+ papers manually takes weeks
- Citation networks are hidden in PDFs
- No way to ask natural questions like *"What papers are most relevant to transformers?"*

---

## ✨ Our Solution: PaperGraph Explorer

**An interactive knowledge graph that lets you click any paper and ask questions in natural language.**

**Demo:** [Open http://localhost:7777]

---

## 🏗️ How It Works (3 Steps)

### Step 1: Download Papers from ArXiv
```bash
python download_papers.py 1706.03762 -n 100
```
- Downloads 100 papers related to "Attention Is All You Need"
- Gets: titles, authors, abstracts, publication dates
- Output: `papers_metadata.json` (680KB)

---

### Step 2: Build Knowledge Graph with Cognee

This is where the magic happens! We use **3 key cognee functions:**

```python
import cognee

# 1. Clear old data from Qdrant
await cognee.prune.prune_data()

# 2. Add papers to cognee (with progress bar!)
for paper in papers:
    text = f"""
    Paper: {paper['title']}
    Authors: {', '.join(paper['authors'])}
    Abstract: {paper['summary']}
    """
    await cognee.add(text, dataset_name="papers")

# 3. Build the knowledge graph
await cognee.cognify()
```

**What happens during `cognee.cognify()`:**
- 🧠 Extracts entities: Papers, Authors, Concepts (transformers, attention, etc.)
- 🔗 Identifies relationships: authored_by, cites, relates_to
- 📊 Generates embeddings using Ollama (nomic-embed-text)
- 💾 Stores everything in Qdrant vector database

**Result:** 6 collections in Qdrant containing:
- Paper chunks with embeddings
- Entity vectors (authors, concepts)
- Graph relationships
- Document summaries

---

### Step 3: Interactive UI + Natural Language Queries

```python
# FastAPI backend serves:
# 1. Graph visualization endpoint
@app.get("/api/graph")
async def get_graph():
    # Returns nodes and edges for vis.js
    return {"nodes": [...], "edges": [...]}

# 2. Natural language query endpoint
@app.post("/api/query")
async def query_paper(paper_id: str, question: str):
    # Uses cognee's GraphCompletionRetriever
    retriever = GraphCompletionRetriever(...)

    # Gets graph context around the paper
    context = await retriever.get_context(query)

    # Converts graph triplets to text
    context_text = await resolve_edges_to_text(triplets)

    # Sends to OpenAI GPT-4 with context
    answer = await openai.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{context_text}\n\nQ: {question}"}
        ]
    )

    return {"answer": answer}
```

---

## 🎨 Live Demo

**[Switch to browser: http://localhost:7777]**

### Demo Flow:

1. **Show the graph**
   - "Here are 100 papers visualized as a knowledge graph"
   - Blue nodes = seed papers (highly relevant)
   - Gray nodes = related papers
   - Arrows show relationships

2. **Click a paper node**
   - "Let's click on the 'Attention Is All You Need' paper"
   - Paper details appear in side panel

3. **Ask a natural language question**
   - Type: *"What are the key contributions of this paper?"*
   - **Show answer appearing in real-time**

4. **Ask another question**
   - Type: *"What are the most relevant papers to this one?"*
   - **GPT-4 answers using graph context**

5. **Click another paper**
   - "The context automatically updates for each paper"
   - Type: *"Who are the main authors?"*

---

## 🔧 Technical Architecture

```
ArXiv API (100 papers)
    ↓
Download metadata (titles, authors, abstracts)
    ↓
cognee.add() → Chunk and embed papers
    ↓
cognee.cognify() → Extract entities & relationships
    ↓
Qdrant (6 collections)
    ├── PaperChunk_text (embeddings)
    ├── Entity_name (authors, concepts)
    ├── EdgeType_relationship_name (graph edges)
    └── TextSummary_text (summaries)
    ↓
FastAPI Backend
    ├── /api/graph → vis.js visualization
    └── /api/query → GraphCompletionRetriever
    ↓
OpenAI GPT-4o-mini (answers with graph context)
    ↓
Interactive UI (click + ask questions)
```

---

## 🧩 Cognee Functions Used

| Function | Purpose | Where Used |
|----------|---------|------------|
| `cognee.prune.prune_data()` | Clear old Qdrant data | `ingest_papers.py:52` |
| `cognee.add(text, dataset_name)` | Add paper text for processing | `ingest_papers.py:70` |
| `cognee.cognify()` | Build knowledge graph | `ingest_papers.py:81` |
| `GraphCompletionRetriever` | Retrieve relevant graph context | `custom_retriever.py:31` |
| `resolve_edges_to_text()` | Convert graph to readable text | `custom_retriever.py:89` |
| `get_graph_engine()` | Access Qdrant graph database | `custom_retriever.py:23` |

---

## 💡 What Makes This Special?

1. **Automatic Knowledge Extraction**
   - No manual tagging or labeling
   - Cognee automatically finds entities and relationships

2. **Semantic Search**
   - Not just keyword matching
   - Understands meaning through embeddings

3. **Interactive Exploration**
   - Click any paper to explore its context
   - Visual graph makes connections obvious

4. **Natural Language Queries**
   - Ask questions like you're talking to a researcher
   - GPT-4 uses graph context for accurate answers

5. **Scalable**
   - Currently: 100 papers
   - Can scale to 1000s with same architecture

---

## 🚀 Tech Stack

- **Knowledge Graph:** [cognee](https://github.com/topoteretes/cognee) - Extract, Cognify, Load pipeline
- **Vector Database:** [Qdrant](https://qdrant.tech) - 6 collections with embeddings + graph
- **Embeddings:** Ollama (nomic-embed-text, 768-dim, local)
- **LLM:** OpenAI GPT-4o-mini (fast, accurate answers)
- **Backend:** FastAPI (async Python API)
- **Frontend:** vis.js (graph visualization) + vanilla JS
- **Data Source:** arXiv API (academic papers)

---

## 📊 By The Numbers

- **100 papers** ingested in ~5 minutes
- **6 Qdrant collections** created
- **2 core cognee functions** (`add`, `cognify`)
- **680KB** of paper metadata
- **Real-time** natural language queries
- **Sub-second** response times

---

## 🎯 Use Cases

**For Researchers:**
- Quickly understand paper landscapes
- Find most relevant papers in a field
- Discover author connections

**For Students:**
- Explore topics visually
- Get summaries of complex papers
- Find reading lists on specific topics

**For Companies:**
- Patent analysis
- Competitive research
- Literature reviews

---

## 🔮 Future Enhancements

1. **Full PDF Ingestion** (currently abstracts only)
2. **Citation Network** (integrate Semantic Scholar API)
3. **Author Network View** (toggle to see collaboration graph)
4. **Time-Based Filtering** (papers by year)
5. **Export Features** (save graphs, export citations)
6. **Multi-Collection Support** (compare different research areas)

---

## ✨ Summary

**PaperGraph Explorer = cognee + Qdrant + GPT-4 + Interactive UI**

**3 cognee functions power everything:**
1. `cognee.add()` - Ingest papers
2. `cognee.cognify()` - Build knowledge graph
3. `GraphCompletionRetriever` - Answer questions with context

**Result:** A research assistant that understands your papers and answers questions naturally.

---

## Questions?

**GitHub:** https://github.com/sucramual/papergraph-explorer-submission

**Try it:** `python3 ingest_papers.py && python3 app.py`

**Thank you!** 🚀
