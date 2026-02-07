# Quick Start: Colored Logging

## Understanding the Logs from `setup.py`

When you run `python setup.py`, you see logs like:

```
2026-02-07T18:29:36.575921 [info] Log file created at: ... [cognee.shared.logging_utils]
2026-02-07T18:29:36.576243 [info] Logging initialized [cognee.shared.logging_utils] cognee_version=0.4.1
```

**These are structlog logs** with:
- 🕒 **Timestamps** (ISO format)
- 📊 **Log levels** (info, warning, error) - automatically colored
- 📦 **Context** (module names, key-value pairs)

---

## Try It Out - 3 Quick Examples

### 1. **Simplest: ANSI Codes** (No installation needed)

```bash
python examples/colored_logging_ansi.py
```

Creates colored output using raw ANSI escape codes - works immediately!

---

### 2. **Best: Rich** (Beautiful UI)

```bash
pip install rich
python examples/colored_logging_rich.py
```

Gets you beautiful tables, panels, progress bars - perfect for CLI tools!

---

### 3. **Production: Structlog** (Like cognee)

```bash
pip install structlog
python examples/colored_logging_structlog.py
```

Production-grade structured logging with automatic coloring.

---

## Enhanced Setup Scripts

### Simple Version (No extra dependencies)
```bash
python examples/simple_colored_setup.py
```

### Beautiful Version (Requires rich)
```bash
pip install rich
python examples/custom_setup_with_colors.py
```

---

## Color Cheat Sheet

### ANSI Codes (copy-paste ready)

```python
# Colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"

# Usage
print(f"{GREEN}✓ Success{RESET}")
print(f"{YELLOW}⚠ Warning{RESET}")
print(f"{RED}✗ Error{RESET}")
```

### Rich Markup (copy-paste ready)

```python
from rich.console import Console
console = Console()

console.print("[green]✓ Success[/green]")
console.print("[yellow]⚠ Warning[/yellow]")
console.print("[red]✗ Error[/red]")
console.print("[cyan]Info[/cyan]")
```

---

## Color Legend

| Color | Meaning | Example |
|-------|---------|---------|
| 🔵 **Cyan/Blue** | Info | `[info]` logs |
| 🟡 **Yellow** | Warning | `[warning]` logs |
| 🔴 **Red** | Error | `[error]` logs |
| 🟢 **Green** | Success | `✓ Complete` |
| ⚪ **Gray/Dim** | Context | Key-value pairs |

---

## Next Steps

1. **Read** `examples/README_LOGGING.md` for detailed comparison
2. **Run** `python examples/demo_all_logging.py` to see all styles
3. **Choose** the approach that fits your needs
4. **Build** something awesome! 🚀
