# Next Steps - Quick Reference

## Phase 1: Setup (You are here)
✅ README.md created
✅ Paper download script ready (../examples/arxiv_related_papers.py)

## Phase 2: Download Papers (5-10 min)

```bash
cd submission

# Copy download script
cp ../examples/arxiv_related_papers.py ./download_papers.py

# Download 50 papers about "Attention is All You Need"
python download_papers.py 1706.03762 -n 50 -o ./papers

# Parse to JSON (create simple parser)
python parse_metadata_to_json.py
# Input: papers/papers_metadata.txt
# Output: papers_metadata.json
```

## Phase 3: Create Project Files (30-40 min)

### Create `parse_metadata.py` (CRITICAL - Do this first!)
Parse papers_metadata.txt → papers_metadata.json

See README.md "Gap Analysis" section for full code.

```bash
python parse_metadata.py
# Verify: ls -lh papers_metadata.json
```

### Create prompts directory
```bash
mkdir -p prompts

cat > prompts/system_prompt.txt << 'EOF'
You are an academic research assistant helping users understand research papers and their relationships.

When answering questions:
- Be precise and cite specific papers when relevant
- Explain relationships between papers (citations, shared authors, similar concepts)
- Use academic language but remain accessible
- If information is not in the context, say so clearly
EOF

cat > prompts/user_prompt.txt << 'EOF'
Context:
{context}

Question: {question}

Please answer the question based on the context provided about academic papers and their relationships.
EOF
```

### Create `.env`
```bash
cat > .env << 'EOF'
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
VECTOR_DB_PROVIDER=qdrant
VECTOR_DB_URL=http://localhost:6333
VECTOR_DB_KEY=
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-...
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed
EMBEDDING_DIMENSIONS=768
EOF
```

### Create `requirements.txt`
```txt
fastapi
uvicorn
python-dotenv
cognee
cognee-community-vector-adapter-qdrant
openai
qdrant-client
```

### Install dependencies
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Create files in order:
1. ✅ `parse_metadata.py` - DONE FIRST
2. ✅ `prompts/` - DONE SECOND
3. `ingest_papers.py` - Cognee ingestion
4. `app.py` - FastAPI backend (with graph extraction)
5. `static/index.html` - Interactive UI
6. `static/style.css` - Styling

### Copy custom_retriever.py
```bash
cp ../custom_retriever.py ./custom_retriever.py
```

## Phase 4: Ingest Papers (10-15 min)

```bash
# Make sure Qdrant is running
docker ps | grep qdrant

# Make sure Ollama is running (for embeddings)
ollama list

# Run ingestion
python ingest_papers.py
# This will take 10-15 min to process 50 papers
```

## Phase 5: Test Backend (5 min)

```bash
# Start server
python app.py

# Test endpoints
curl http://localhost:7777/api/graph
curl -X POST http://localhost:7777/api/query \
  -H "Content-Type: application/json" \
  -d '{"paper_id": "1706.03762", "question": "What is this paper about?"}'
```

## Phase 6: Build UI (20-30 min)

1. Create `static/index.html` with vis.js graph
2. Implement node click handling
3. Add query interface
4. Style with CSS

## Phase 7: Demo (10 min)

1. Open http://localhost:7777
2. Click on "Attention is All You Need" paper
3. Ask: "What are the most influential related papers?"
4. Show answer
5. Click another paper and repeat

---

## Key Commands

```bash
# Download papers
python download_papers.py 1706.03762 -n 50 -o ./papers

# Ingest papers
python ingest_papers.py

# Start server
python app.py

# Open browser
open http://localhost:7777
```

---

## Troubleshooting

### Qdrant not running
```bash
docker start qdrant
# or
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 \
  -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

### Ollama not running
```bash
brew services start ollama  # Mac
sudo systemctl start ollama # Linux
```

### Import errors
```bash
uv pip install -r requirements.txt
```

---

## Timeline (Updated with gaps)

- [ ] Download papers: 10 min
- [ ] **Parse metadata (NEW)**: 5 min
- [ ] **Create prompts (NEW)**: 5 min
- [ ] Create files: 30 min
- [ ] Ingest papers: 15 min
- [ ] **Graph extraction logic (NEW)**: 15 min
- [ ] Build UI: 25 min
- [ ] Test: 15 min
- [ ] Polish: 10 min

**Total: ~2 hours (still on track!)**

## Critical Path

```
parse_metadata.py → papers_metadata.json
    ↓
prompts/ created
    ↓
ingest_papers.py → Qdrant collections
    ↓
app.py (with graph extraction) → API working
    ↓
static/index.html → UI connected
    ↓
End-to-end test → Demo ready
```
