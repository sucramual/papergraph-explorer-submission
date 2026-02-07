# arXiv Related Papers Finder

Find and download papers related to any arXiv paper using multiple strategies.

## Installation

The script uses only Python standard library, no additional dependencies needed!

## Usage

### Basic Usage

Find 50 related papers for a given arXiv ID:

```bash
python arxiv_related_papers.py 2103.14030
```

### Custom Number of Papers

Find a specific number of papers (e.g., 100):

```bash
python arxiv_related_papers.py 2103.14030 -n 100
```

### Search Strategies

Choose different strategies to find related papers:

```bash
# By category only (fastest)
python arxiv_related_papers.py 2103.14030 -s category

# By authors only
python arxiv_related_papers.py 2103.14030 -s authors

# By keywords only
python arxiv_related_papers.py 2103.14030 -s keywords

# Mixed (default - uses all strategies)
python arxiv_related_papers.py 2103.14030 -s mixed
```

### Download PDFs

To actually download the PDF files (warning: can be slow):

```bash
python arxiv_related_papers.py 2103.14030 --download-pdfs
```

### Custom Output Directory

```bash
python arxiv_related_papers.py 2103.14030 -o ./my_papers --download-pdfs
```

## Examples

### Example 1: Find 50 related papers (metadata only)

```bash
python arxiv_related_papers.py 1706.03762 -n 50
```

This will:
- Fetch metadata for the "Attention is All You Need" paper
- Search for related papers by category, authors, and keywords
- Save metadata to `./arxiv_papers/papers_metadata.txt`

### Example 2: Download 20 papers from same category

```bash
python arxiv_related_papers.py 2010.11929 -n 20 -s category --download-pdfs
```

### Example 3: Find papers by same authors

```bash
python arxiv_related_papers.py 1706.03762 -s authors -n 30 --download-pdfs
```

## Output

The script creates a directory (default: `./arxiv_papers/`) containing:

1. **papers_metadata.txt** - Text file with all paper metadata including:
   - Paper ID
   - Title
   - Authors
   - Publication date
   - Abstract
   - PDF URL

2. **PDF files** (if `--download-pdfs` is used) - Named by arXiv ID

## Rate Limiting

The script automatically includes 3-second delays between API calls to respect arXiv's rate limits.

## Common arXiv Paper IDs to Try

- `1706.03762` - Attention is All You Need (Transformers)
- `2010.11929` - CLIP (Vision-Language)
- `2103.14030` - DALL-E (Text-to-Image)
- `1810.04805` - BERT (NLP)
- `2005.14165` - GPT-3
- `2303.08774` - GPT-4 Technical Report
- `1512.03385` - ResNet (Computer Vision)

## Tips

1. **Start without PDFs**: First run without `--download-pdfs` to see the metadata, then download only if needed
2. **Use category search**: If you want papers from the same field, use `-s category` for faster results
3. **Check the metadata file**: Review `papers_metadata.txt` before downloading to see if the papers are relevant
4. **Be patient**: Downloading many PDFs can take time due to rate limiting
