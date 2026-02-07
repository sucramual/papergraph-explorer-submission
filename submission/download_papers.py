#!/usr/bin/env python3
"""
Script to find and download related papers from arXiv based on a seed paper.
Uses the arXiv API to search by authors, categories, and keywords.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
import re
import os
from pathlib import Path
from typing import List, Dict, Optional
import argparse


class ArxivRelatedPapersFinder:
    """Finds papers related to a seed paper using arXiv API."""

    BASE_URL = "http://export.arxiv.org/api/query"
    NAMESPACES = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }

    def __init__(self, output_dir: str = "./arxiv_papers"):
        self.output_dir = Path(output_dir).expanduser().resolve()
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            if e.errno == 30:  # Read-only file system
                print(f"Error: Cannot create directory '{self.output_dir}' - file system is read-only")
                print("Please specify a writable directory using -o option")
                print("Example: -o ./papers or -o ~/arxiv_papers")
                raise SystemExit(1)
            elif e.errno == 13:  # Permission denied
                print(f"Error: Permission denied to create directory '{self.output_dir}'")
                print("Please specify a directory where you have write permissions using -o option")
                raise SystemExit(1)
            else:
                print(f"Error creating output directory '{self.output_dir}': {e}")
                raise

        # Verify directory is writable
        if not os.access(self.output_dir, os.W_OK):
            print(f"Error: Directory '{self.output_dir}' is not writable")
            print("Please specify a writable directory using -o option")
            raise SystemExit(1)

    def fetch_paper_metadata(self, arxiv_id: str) -> Optional[Dict]:
        """Fetch metadata for a specific arXiv paper."""
        # Clean the arxiv_id (remove version if present)
        arxiv_id = arxiv_id.split('v')[0]

        url = f"{self.BASE_URL}?id_list={arxiv_id}"

        try:
            with urllib.request.urlopen(url) as response:
                xml_data = response.read().decode('utf-8')

            root = ET.fromstring(xml_data)
            entry = root.find('atom:entry', self.NAMESPACES)

            if entry is None:
                print(f"Paper {arxiv_id} not found")
                return None

            # Extract metadata
            metadata = {
                'id': entry.find('atom:id', self.NAMESPACES).text,
                'title': entry.find('atom:title', self.NAMESPACES).text.strip(),
                'summary': entry.find('atom:summary', self.NAMESPACES).text.strip(),
                'authors': [author.find('atom:name', self.NAMESPACES).text
                           for author in entry.findall('atom:author', self.NAMESPACES)],
                'categories': [cat.get('term')
                             for cat in entry.findall('atom:category', self.NAMESPACES)],
                'pdf_url': None
            }

            # Get PDF URL
            for link in entry.findall('atom:link', self.NAMESPACES):
                if link.get('title') == 'pdf':
                    metadata['pdf_url'] = link.get('href')
                    break

            return metadata

        except Exception as e:
            print(f"Error fetching paper metadata: {e}")
            return None

    def extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """Extract important keywords from title/abstract."""
        # Remove common words and extract meaningful terms
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                       'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
                       'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                       'do', 'does', 'did', 'will', 'would', 'could', 'should',
                       'this', 'that', 'these', 'those', 'we', 'our', 'using'}

        # Simple keyword extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        keywords = [w for w in words if w not in common_words]

        # Return most frequent keywords
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [word for word, _ in keyword_counts.most_common(max_keywords)]

    def search_related_papers(self,
                            query: str,
                            max_results: int = 50,
                            sort_by: str = 'relevance') -> List[Dict]:
        """Search for papers using a query string."""
        params = {
            'search_query': query,
            'max_results': max_results,
            'sortBy': sort_by,
            'sortOrder': 'descending'
        }

        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"

        try:
            with urllib.request.urlopen(url) as response:
                xml_data = response.read().decode('utf-8')

            root = ET.fromstring(xml_data)
            entries = root.findall('atom:entry', self.NAMESPACES)

            papers = []
            for entry in entries:
                paper = {
                    'id': entry.find('atom:id', self.NAMESPACES).text.split('/')[-1],
                    'title': entry.find('atom:title', self.NAMESPACES).text.strip(),
                    'summary': entry.find('atom:summary', self.NAMESPACES).text.strip(),
                    'authors': [author.find('atom:name', self.NAMESPACES).text
                               for author in entry.findall('atom:author', self.NAMESPACES)],
                    'published': entry.find('atom:published', self.NAMESPACES).text,
                    'pdf_url': None
                }

                # Get PDF URL
                for link in entry.findall('atom:link', self.NAMESPACES):
                    if link.get('title') == 'pdf':
                        paper['pdf_url'] = link.get('href')
                        break

                papers.append(paper)

            return papers

        except Exception as e:
            print(f"Error searching papers: {e}")
            return []

    def find_related_papers(self,
                          arxiv_id: str,
                          max_results: int = 50,
                          strategy: str = 'mixed') -> List[Dict]:
        """
        Find papers related to a seed paper.

        Strategies:
        - 'category': Search papers in same categories
        - 'authors': Search papers by same authors
        - 'keywords': Search papers with similar keywords
        - 'mixed': Combine all strategies (default)
        """
        print(f"Fetching metadata for paper: {arxiv_id}")
        seed_paper = self.fetch_paper_metadata(arxiv_id)

        if not seed_paper:
            return []

        print(f"\nSeed Paper: {seed_paper['title']}")
        print(f"Authors: {', '.join(seed_paper['authors'][:3])}")
        print(f"Categories: {', '.join(seed_paper['categories'])}")

        related_papers = []

        if strategy in ['category', 'mixed']:
            # Search by primary category
            if seed_paper['categories']:
                primary_cat = seed_paper['categories'][0]
                print(f"\nSearching papers in category: {primary_cat}")
                cat_papers = self.search_related_papers(
                    f"cat:{primary_cat}",
                    max_results=max_results
                )
                related_papers.extend(cat_papers)
                print(f"Found {len(cat_papers)} papers by category")
                time.sleep(3)  # Rate limiting

        if strategy in ['authors', 'mixed']:
            # Search by first author
            if seed_paper['authors']:
                first_author = seed_paper['authors'][0]
                print(f"\nSearching papers by author: {first_author}")
                author_papers = self.search_related_papers(
                    f"au:{first_author}",
                    max_results=min(20, max_results)
                )
                related_papers.extend(author_papers)
                print(f"Found {len(author_papers)} papers by author")
                time.sleep(3)  # Rate limiting

        if strategy in ['keywords', 'mixed']:
            # Search by keywords
            keywords = self.extract_keywords(
                seed_paper['title'] + " " + seed_paper['summary']
            )
            if keywords:
                keyword_query = " AND ".join([f"all:{kw}" for kw in keywords[:3]])
                print(f"\nSearching papers with keywords: {', '.join(keywords[:3])}")
                keyword_papers = self.search_related_papers(
                    keyword_query,
                    max_results=min(30, max_results)
                )
                related_papers.extend(keyword_papers)
                print(f"Found {len(keyword_papers)} papers by keywords")
                time.sleep(3)  # Rate limiting

        # Remove duplicates (keep first occurrence)
        seen_ids = set()
        unique_papers = []
        for paper in related_papers:
            if paper['id'] not in seen_ids:
                seen_ids.add(paper['id'])
                unique_papers.append(paper)

        print(f"\nTotal unique related papers found: {len(unique_papers)}")
        return unique_papers[:max_results]

    def download_pdf(self, pdf_url: str, filename: str) -> bool:
        """Download a PDF from arXiv."""
        filepath = self.output_dir / filename

        try:
            print(f"Downloading: {filename}")
            urllib.request.urlretrieve(pdf_url, filepath)
            return True
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            return False

    def save_metadata(self, papers: List[Dict], filename: str = "papers_metadata.txt"):
        """Save paper metadata to a text file."""
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            for i, paper in enumerate(papers, 1):
                f.write(f"\n{'='*80}\n")
                f.write(f"Paper {i}\n")
                f.write(f"{'='*80}\n")
                f.write(f"ID: {paper['id']}\n")
                f.write(f"Title: {paper['title']}\n")
                f.write(f"Authors: {', '.join(paper['authors'])}\n")
                f.write(f"Published: {paper.get('published', 'N/A')}\n")
                f.write(f"PDF URL: {paper['pdf_url']}\n")
                f.write(f"\nAbstract:\n{paper['summary']}\n")

        print(f"\nMetadata saved to: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description='Find and download papers related to an arXiv paper'
    )
    parser.add_argument('arxiv_id', help='arXiv paper ID (e.g., 2103.14030)')
    parser.add_argument(
        '-n', '--num-papers',
        type=int,
        default=50,
        help='Number of related papers to find (default: 50)'
    )
    parser.add_argument(
        '-s', '--strategy',
        choices=['category', 'authors', 'keywords', 'mixed'],
        default='mixed',
        help='Search strategy (default: mixed)'
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='./arxiv_papers',
        help='Output directory for papers (default: ./arxiv_papers)'
    )
    parser.add_argument(
        '--download-pdfs',
        action='store_true',
        help='Download PDF files (can be slow)'
    )

    args = parser.parse_args()

    # Create finder instance
    finder = ArxivRelatedPapersFinder(output_dir=args.output_dir)

    # Find related papers
    related_papers = finder.find_related_papers(
        args.arxiv_id,
        max_results=args.num_papers,
        strategy=args.strategy
    )

    if not related_papers:
        print("No related papers found.")
        return

    # Save metadata
    finder.save_metadata(related_papers)

    # Download PDFs if requested
    if args.download_pdfs:
        print(f"\nDownloading {len(related_papers)} PDFs...")
        for i, paper in enumerate(related_papers, 1):
            if paper['pdf_url']:
                filename = f"{paper['id'].replace('/', '_')}.pdf"
                finder.download_pdf(paper['pdf_url'], filename)
                time.sleep(3)  # Rate limiting

                if i % 10 == 0:
                    print(f"Progress: {i}/{len(related_papers)}")

        print(f"\nAll papers downloaded to: {finder.output_dir}")
    else:
        print("\nTo download PDFs, run again with --download-pdfs flag")


if __name__ == "__main__":
    main()
