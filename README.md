# AI Memory Hackathon

**Submission:** See [`submission/`](submission/) folder for the PaperGraph Explorer project.

---

## Quick Setup

Install Ollama, Python environment, and Qdrant:

```bash
# Ollama installation
brew install ollama   # macOS
ollama serve &

# Ollama models (from USB)
cd models
ollama create nomic-embed-text -f nomic-embed-text/Modelfile
ollama create cognee-distillabs-model-gguf-quantized -f cognee-distillabs-model-gguf-quantized/Modelfile
cd ..

# Python environment
uv venv
source .venv/bin/activate
uv sync

# Graph setup
python setup.py

# Qdrant (local Docker)
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 \
  -v qdrant_storage:/qdrant/storage qdrant/qdrant

# Configure and restore data
cp .env.example.local .env
uv run python download-from-spaces.py
uv run python restore-snapshots.py

# Test Q&A
python solution_q_and_a.py
```

---

## What's Included

### Data (After Restore)
14,837 vectors across 6 Qdrant collections:
- DocumentChunk_text (2,000 records) - Invoice/transaction chunks
- Entity_name (8,816 records) - Products, vendors, SKUs
- EntityType_name (8 records) - Entity types
- EdgeType_relationship_name (13 records) - Relationship types
- TextDocument_name (2,000 records) - Document references
- TextSummary_text (2,000 records) - Document summaries

### Models
- **nomic-embed-text** - 768-dim embeddings
- **Distil Labs SLM** - Fine-tuned reasoning model (GGUF)
- **Qwen3-4B** - Fallback LLM (optional)

---

## Example Projects

Three FastAPI demo projects included:
- **project1-procurement-search** (port 7777) - Semantic search with interactive UI
- **project2-spend-analytics** (port 5553) - Analytics dashboard with Chart.js
- **project3-anomaly-detective** (port 6971) - Automated anomaly detection

Run any project:
```bash
cd project1-procurement-search
uv sync
uv run python app.py
```

---

## Architecture

```
Raw documents
    ↓
cognee.add() + cognee.cognify()     # Extract entities, relationships
    ↓
Qdrant (6 collections)              # Vector + graph storage
    ↓
FastAPI apps                         # Custom applications
    ↓
Distil Labs SLM / OpenAI            # LLM reasoning
```

---

## Useful Commands

### Ollama (macOS)
```bash
brew services start ollama
brew services stop ollama
```

### Ollama (Linux)
```bash
sudo systemctl start ollama
sudo systemctl stop ollama
```

### Qdrant Docker
```bash
# Stop and remove
docker stop qdrant && docker rm qdrant
docker volume rm qdrant_storage

# Restart
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 \
  -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

---

## Adding Your Own Data

```python
import cognee
from cognee.api.v1.search import SearchType

# Add and process documents
await cognee.add("Your document text here...")
await cognee.cognify()

# Search
results = await cognee.search(
    query_text="What vendors supply IT equipment?",
    query_type=SearchType.CHUNKS,
)

# Reset
await cognee.prune.prune_data()
await cognee.prune.prune_system(metadata=True)
```

See [cognee docs](https://docs.cognee.ai) for full API reference.

---

## Using Qdrant Cloud (Alternative)

For hosted Qdrant instead of local Docker:

```bash
cp .env.example .env
# Edit .env: add QDRANT_URL and QDRANT_API_KEY from cloud.qdrant.io
uv run python download-from-spaces.py
uv run python restore-snapshots.py
```

Create free cluster: [cloud.qdrant.io](https://cloud.qdrant.io)

---

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/)
- Docker (for local Qdrant)

---

## Hackathon Constraints

- ✅ Qdrant as vector store (local or hosted)
- ✅ Local model must remain functional
- ✅ Raw data in `data/` folder for reference only

---

## Submission

**PaperGraph Explorer** - Interactive knowledge graph for academic papers with natural language queries.

📂 Location: [`submission/`](submission/)
📖 Documentation: [submission/README.md](submission/README.md)

**Stack:** cognee + Qdrant + OpenAI + vis.js + FastAPI

---

**Built with [cognee](https://github.com/topoteretes/cognee) + [Qdrant](https://qdrant.tech) + [Distil Labs](https://www.distillabs.ai/)**
