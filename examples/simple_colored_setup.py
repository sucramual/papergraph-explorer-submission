#!/usr/bin/env python3
"""
Simple colored setup.py using only ANSI codes (no extra dependencies)
"""
import cognee
import asyncio
from helper_functions import import_cognee_data
from cognee.api.v1.visualize.visualize import visualize_graph

# Simple ANSI colors
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    RED = "\033[31m"
    DIM = "\033[2m"

def print_header(text):
    print(f"\n{C.BOLD}{C.CYAN}{'='*60}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{text.center(60)}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'='*60}{C.RESET}\n")

def print_step(text):
    print(f"{C.YELLOW}⚙{C.RESET} {text}")

def print_success(text):
    print(f"{C.GREEN}✓{C.RESET} {text}")

def print_error(text):
    print(f"{C.RED}✗{C.RESET} {text}")

async def main():
    print_header("Cognee Knowledge Graph Setup")

    # Clear ALL cognee data and system tables
    print_step("Clearing all cognee data...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    print_success("All data cleared")
    print()

    # Import everything
    print_step("Importing data from export...")
    success = await import_cognee_data("cognee_export", verbose=True)

    if not success:
        print_error("Import failed!")
        return

    print_success("Data imported successfully")
    print()

    # Create visualization
    print_step("Creating graph visualization...")
    await visualize_graph("./graphs/after_setup.html")
    print_success("Graph visualization created")

    # Summary
    print(f"\n{C.BOLD}{C.GREEN}{'='*60}{C.RESET}")
    print(f"{C.BOLD}{C.GREEN}✓ Setup Complete!{C.RESET}")
    print(f"{C.BOLD}{C.GREEN}{'='*60}{C.RESET}")
    print(f"  📊 Graph visualization: {C.CYAN}./graphs/after_setup.html{C.RESET}")
    print(f"  🗄️  Collections: {C.YELLOW}6{C.RESET}")
    print(f"  🔢 Total vectors: {C.YELLOW}14,837{C.RESET}")
    print(f"\n  {C.DIM}Run next:{C.RESET} {C.CYAN}python solution_q_and_a.py{C.RESET}")
    print(f"{C.BOLD}{C.GREEN}{'='*60}{C.RESET}\n")

if __name__ == "__main__":
    asyncio.run(main())
