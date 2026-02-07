#!/bin/bash
# Quick start script for PaperGraph Explorer

echo "🚀 Starting PaperGraph Explorer..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Please create .env file with your OpenAI API key:"
    echo ""
    echo "cp .env.example .env"
    echo "# Then edit .env and add your OPENAI_API_KEY"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/installed" ]; then
    echo "📦 Installing dependencies..."
    uv pip install -r requirements.txt
    touch .venv/installed
fi

# Check if papers have been ingested
if [ ! -d "../.venv/lib/python3.12/site-packages/cognee/.cognee_system" ]; then
    echo ""
    echo "⚠️  Papers not yet ingested!"
    echo "Please run: python3 ingest_papers.py"
    echo ""
    read -p "Run ingestion now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 ingest_papers.py
    else
        exit 1
    fi
fi

# Start server
echo ""
echo "✓ Starting server on http://localhost:7777"
echo "  Press Ctrl+C to stop"
echo ""
python3 app.py
