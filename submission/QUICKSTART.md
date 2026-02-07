# PaperGraph Explorer - Quick Start

**Status:** ✅ All code complete and ready to run

---

## Prerequisites

✅ Papers downloaded (500 papers in `data/papers_metadata.txt`)
✅ Papers parsed to JSON (`papers_metadata.json`)
✅ All code files created

**Still needed:**
- OpenAI API key
- Qdrant running (Docker)
- Ollama running (for embeddings)

---

## Setup (5 minutes)

### 1. Configure Environment

```bash
cd submission

# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# nano .env
# or
# code .env
```

**Required:**
- `OPENAI_API_KEY=sk-your-key-here`

### 2. Start Services

```bash
# Start Qdrant (if not running)
docker start qdrant
# or
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 \
  -v qdrant_storage:/qdrant/storage qdrant/qdrant

# Start Ollama (if not running)
brew services start ollama  # macOS
# or
sudo systemctl start ollama  # Linux

# Verify services
docker ps | grep qdrant
curl http://localhost:11434/api/tags
```

### 3. Install Dependencies

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install packages
uv pip install -r requirements.txt
```

---

## Run (2 steps)

### Step 1: Ingest Papers (15 minutes, one-time)

```bash
python3 ingest_papers.py
```

This will:
- Clear old cognee data
- Ingest 50 papers into cognee
- Build knowledge graph
- Store vectors in Qdrant

**⏱️ Takes 10-15 minutes** - grab coffee!

### Step 2: Start Server

```bash
python3 app.py
```

Or use the run script:
```bash
./run.sh
```

---

## Demo (Open Browser)

Open: **http://localhost:7777**

You'll see:
1. **Interactive graph** with 50 papers (nodes)
   - Blue nodes = seed papers (highly relevant)
   - Gray nodes = related papers
2. **Click any paper node**
3. **Ask questions:**
   - "What are the key contributions?"
   - "What are the most relevant papers to this?"
   - "Who are the main authors?"
4. **Get AI-powered answers** using OpenAI + knowledge graph context

---

## Troubleshooting

### Qdrant not running
```bash
docker ps -a | grep qdrant
docker start qdrant
```

### Ollama not running
```bash
brew services start ollama
ollama list  # Should show nomic-embed-text
```

### OpenAI API errors
- Check `.env` has correct `OPENAI_API_KEY`
- Verify API key at: https://platform.openai.com/api-keys
- Check credits: https://platform.openai.com/usage

### Graph not showing
- Open browser console (F12)
- Check for JavaScript errors
- Verify `/api/graph` returns data:
  ```bash
  curl http://localhost:7777/api/graph
  ```

### Import errors
```bash
source .venv/bin/activate
uv pip install -r requirements.txt
```

---

## Project Structure

```
submission/
├── data/
│   └── papers_metadata.txt      # Downloaded papers (500)
├── papers_metadata.json         # Parsed JSON (500)
├── prompts/
│   ├── system_prompt.txt
│   └── user_prompt.txt
├── static/
│   ├── index.html               # Interactive UI
│   └── style.css
├── parse_metadata.py            # ✅ DONE
├── ingest_papers.py             # Run this first
├── app.py                       # FastAPI server
├── custom_retriever.py
├── custom_generate_completion.py
├── requirements.txt
├── .env.example
├── .env                         # YOU CREATE THIS
└── run.sh
```

---

## Architecture

```
Papers (JSON) → cognee.add() → Knowledge Graph → Qdrant
                                       ↓
User clicks paper → FastAPI → Custom Retriever → OpenAI GPT-4
                                       ↓
                              Graph context + Question
                                       ↓
                                Natural Language Answer
```

---

## Next Steps After Demo

- Add more papers (change `papers = all_papers[:50]` to `:100`)
- Improve graph layout
- Add paper search
- Add author network view
- Deploy to cloud

---

## Time Breakdown

- ✅ Setup environment: 5 min
- ✅ Ingest papers: 15 min
- ✅ Start server: 1 min
- ✅ Demo: 5 min

**Total: ~25 minutes from setup to working demo**

---

**Built with:** cognee + Qdrant + OpenAI + vis.js + FastAPI

**Demo-ready!** 🚀
