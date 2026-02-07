"""
Example: Beautiful colored logging with rich
"""
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import logging
import time

# Setup rich console
console = Console()

# Setup logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, console=console)]
)

logger = logging.getLogger("rich_example")

# Example usage
if __name__ == "__main__":
    # Basic logging
    logger.info("Application started", extra={"version": "1.0.0"})
    logger.warning("Configuration file not found")
    logger.error("Failed to connect to database")

    # Rich console methods
    console.print("[bold green]✓[/bold green] Setup complete")
    console.print("[bold yellow]⚠[/bold yellow] Warning: Using defaults")
    console.print("[bold red]✗[/bold red] Error occurred")

    # Panels
    console.print(Panel.fit(
        "[green]Graph restored successfully[/green]\n"
        "Collections: 6\n"
        "Vectors: 14,837",
        title="Setup Status",
        border_style="green"
    ))

    # Progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Restoring snapshots...", total=6)
        for i in range(6):
            time.sleep(0.3)
            progress.update(task, advance=1)

    console.print("[bold green]✓ All snapshots restored[/bold green]")
