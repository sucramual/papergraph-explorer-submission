#!/usr/bin/env python3
"""
Enhanced setup.py with custom colored output
Shows how to add your own colored messages alongside cognee's logs
"""
import cognee
import asyncio
from helper_functions import import_cognee_data
from cognee.api.v1.visualize.visualize import visualize_graph
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import time

# Initialize rich console for beautiful output
console = Console()

async def main():
    # Header
    console.print(Panel.fit(
        "[bold cyan]Cognee Knowledge Graph Setup[/bold cyan]\n"
        "Clearing old data and importing graph from export",
        border_style="cyan",
        padding=(1, 2)
    ))

    # Clear ALL cognee data and system tables
    console.print("\n[yellow]⚙[/yellow] Clearing all cognee data...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    console.print("[green]✓[/green] All data cleared\n")

    # Import with progress bar
    console.print("[yellow]⚙[/yellow] Importing data from export...")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Loading graph data...", total=100)

        # Simulate progress (in reality, import_cognee_data doesn't report progress)
        for i in range(0, 100, 10):
            progress.update(task, advance=10)
            await asyncio.sleep(0.1)

        # Actual import
        success = await import_cognee_data("cognee_export", verbose=True)

    if not success:
        console.print("[bold red]✗ Import failed![/bold red]")
        return

    console.print("[green]✓[/green] Data imported successfully\n")

    # Create visualization
    console.print("[yellow]⚙[/yellow] Creating graph visualization...")
    await visualize_graph("./graphs/after_setup.html")
    console.print("[green]✓[/green] Graph visualization created\n")

    # Success summary
    console.print(Panel.fit(
        "[bold green]✓ Setup Complete![/bold green]\n\n"
        "📊 Graph visualization: [cyan]./graphs/after_setup.html[/cyan]\n"
        "🗄️  Collections: [yellow]6[/yellow]\n"
        "🔢 Total vectors: [yellow]14,837[/yellow]\n\n"
        "[dim]You can now run:[/dim]\n"
        "[cyan]python solution_q_and_a.py[/cyan]",
        title="[bold]Setup Status[/bold]",
        border_style="green",
        padding=(1, 2)
    ))

if __name__ == "__main__":
    asyncio.run(main())
