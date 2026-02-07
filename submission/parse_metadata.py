#!/usr/bin/env python3
"""
Parse papers_metadata.txt to JSON format.
Converts the text output from arXiv download script to structured JSON.
"""
import re
import json

def parse_metadata_txt(filepath):
    """Parse papers_metadata.txt to JSON."""
    with open(filepath) as f:
        content = f.read()

    # Split by paper separator
    paper_blocks = content.split('='*80)[1:]  # Skip empty first

    papers = []
    for block in paper_blocks:
        if not block.strip():
            continue

        # Extract fields with regex
        paper = {}

        id_match = re.search(r'ID: (.+)', block)
        if id_match:
            paper['id'] = id_match.group(1).strip()

        title_match = re.search(r'Title: (.+)', block)
        if title_match:
            paper['title'] = title_match.group(1).strip()

        authors_match = re.search(r'Authors: (.+)', block)
        if authors_match:
            paper['authors'] = [a.strip() for a in authors_match.group(1).split(',')]

        pub_match = re.search(r'Published: (.+)', block)
        if pub_match:
            paper['published'] = pub_match.group(1).strip()

        pdf_match = re.search(r'PDF URL: (.+)', block)
        if pdf_match:
            paper['pdf_url'] = pdf_match.group(1).strip()

        abstract_match = re.search(r'Abstract:\n(.+)', block, re.DOTALL)
        if abstract_match:
            paper['summary'] = abstract_match.group(1).strip()

        if paper:
            papers.append(paper)

    return papers

if __name__ == "__main__":
    print("Parsing papers_metadata.txt...")
    papers = parse_metadata_txt("data/papers_metadata.txt")

    with open("papers_metadata.json", "w") as f:
        json.dump(papers, f, indent=2)

    print(f"✓ Parsed {len(papers)} papers to papers_metadata.json")

    # Show first paper as sample
    if papers:
        print(f"\nSample paper:")
        print(f"  ID: {papers[0]['id']}")
        print(f"  Title: {papers[0]['title'][:60]}...")
        print(f"  Authors: {', '.join(papers[0]['authors'][:3])}")
