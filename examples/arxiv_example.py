#!/usr/bin/env python3
"""
Example usage of the ArxivRelatedPapersFinder as a library.
"""

from arxiv_related_papers import ArxivRelatedPapersFinder


def example_basic_usage():
    """Basic example: Find related papers and save metadata."""
    print("=" * 80)
    print("Example 1: Basic Usage - Find 50 related papers")
    print("=" * 80)

    # Create finder instance
    finder = ArxivRelatedPapersFinder(output_dir="./example_papers")

    # Find related papers for the "Attention is All You Need" paper
    arxiv_id = "1706.03762"
    related_papers = finder.find_related_papers(arxiv_id, max_results=50)

    # Save metadata
    finder.save_metadata(related_papers, "attention_related_papers.txt")

    print(f"\nFound {len(related_papers)} related papers")
    print("\nFirst 3 papers:")
    for i, paper in enumerate(related_papers[:3], 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'][:2])}")
        print(f"   ID: {paper['id']}")


def example_category_search():
    """Search papers in same category only."""
    print("\n" + "=" * 80)
    print("Example 2: Category-based Search")
    print("=" * 80)

    finder = ArxivRelatedPapersFinder(output_dir="./example_papers")

    # Search by category only
    arxiv_id = "2010.11929"  # CLIP paper
    related_papers = finder.find_related_papers(
        arxiv_id,
        max_results=30,
        strategy='category'
    )

    print(f"\nFound {len(related_papers)} papers in same category")


def example_author_search():
    """Search papers by same authors."""
    print("\n" + "=" * 80)
    print("Example 3: Author-based Search")
    print("=" * 80)

    finder = ArxivRelatedPapersFinder(output_dir="./example_papers")

    # Search by authors
    arxiv_id = "1810.04805"  # BERT paper
    related_papers = finder.find_related_papers(
        arxiv_id,
        max_results=20,
        strategy='authors'
    )

    print(f"\nFound {len(related_papers)} papers by same authors")


def example_download_specific_papers():
    """Download specific papers only."""
    print("\n" + "=" * 80)
    print("Example 4: Download Specific Papers")
    print("=" * 80)

    finder = ArxivRelatedPapersFinder(output_dir="./example_papers")

    # Find papers
    arxiv_id = "1706.03762"
    related_papers = finder.find_related_papers(
        arxiv_id,
        max_results=100,
        strategy='mixed'
    )

    # Filter papers (e.g., only papers with "transformer" in title)
    filtered_papers = [
        p for p in related_papers
        if 'transformer' in p['title'].lower()
    ]

    print(f"\nFiltered to {len(filtered_papers)} papers with 'transformer' in title")

    # Download only filtered papers
    if filtered_papers:
        print("\nDownloading filtered papers...")
        for paper in filtered_papers[:5]:  # Download first 5
            if paper['pdf_url']:
                filename = f"{paper['id'].replace('/', '_')}.pdf"
                finder.download_pdf(paper['pdf_url'], filename)


def example_get_paper_info():
    """Get information about a specific paper."""
    print("\n" + "=" * 80)
    print("Example 5: Get Paper Metadata")
    print("=" * 80)

    finder = ArxivRelatedPapersFinder()

    # Get metadata for a specific paper
    paper = finder.fetch_paper_metadata("1706.03762")

    if paper:
        print(f"\nTitle: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Categories: {', '.join(paper['categories'])}")
        print(f"\nAbstract: {paper['summary'][:200]}...")


def example_custom_processing():
    """Example with custom processing of results."""
    print("\n" + "=" * 80)
    print("Example 6: Custom Processing")
    print("=" * 80)

    finder = ArxivRelatedPapersFinder(output_dir="./example_papers")

    # Find papers
    related_papers = finder.find_related_papers("2010.11929", max_results=50)

    # Group by publication year
    from collections import defaultdict
    papers_by_year = defaultdict(list)

    for paper in related_papers:
        year = paper['published'][:4]  # Extract year from date
        papers_by_year[year].append(paper)

    print("\nPapers by year:")
    for year in sorted(papers_by_year.keys(), reverse=True):
        print(f"  {year}: {len(papers_by_year[year])} papers")

    # Find most common authors
    from collections import Counter
    all_authors = []
    for paper in related_papers:
        all_authors.extend(paper['authors'])

    author_counts = Counter(all_authors)
    print("\nTop 5 most common authors:")
    for author, count in author_counts.most_common(5):
        print(f"  {author}: {count} papers")


if __name__ == "__main__":
    # Run examples
    # Uncomment the ones you want to try

    example_basic_usage()

    # example_category_search()

    # example_author_search()

    # example_download_specific_papers()

    # example_get_paper_info()

    # example_custom_processing()
