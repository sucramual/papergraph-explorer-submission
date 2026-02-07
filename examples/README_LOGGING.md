# Colored Logging Examples

This directory contains examples of different approaches to create colored console output in Python.

## What You're Seeing in setup.py

The logs from `setup.py` use **structlog** with these features:
- **ISO timestamps**: `2026-02-07T18:29:36.575921`
- **Log levels**: `[info]`, `[warning]`, `[error]`
- **Automatic coloring**: Blue (info), Yellow (warning), Red (error)
- **Structured context**: Key-value pairs like `cognee_version=0.4.1`
- **Module tracking**: `[cognee.shared.logging_utils]`

## Four Approaches

### 1. **structlog** (What cognee uses) ⭐
**File:** `colored_logging_structlog.py`

**Pros:**
- Production-ready structured logging
- Automatic key-value formatting
- JSON output support
- Integrates with standard logging

**Install:**
```bash
pip install structlog
```

**Use when:** Building production applications with complex logging needs

---

### 2. **colorama** (Simple & Cross-platform)
**File:** `colored_logging_colorama.py`

**Pros:**
- Works on Windows, Mac, Linux
- Simple API
- No complex configuration
- Lightweight

**Install:**
```bash
pip install colorama
```

**Use when:** Simple scripts needing basic colored output

---

### 3. **rich** (Beautiful & Feature-rich) ✨
**File:** `colored_logging_rich.py`

**Pros:**
- Beautiful tables, panels, progress bars
- Markdown rendering
- Syntax highlighting
- Tree views
- Enhanced tracebacks

**Install:**
```bash
pip install rich
```

**Use when:** CLI apps where presentation matters

---

### 4. **ANSI codes** (No dependencies)
**File:** `colored_logging_ansi.py`

**Pros:**
- Zero dependencies
- Fast
- Full control
- Works on Mac/Linux

**Cons:**
- Doesn't work well on Windows (use colorama instead)

**Use when:** Minimal dependencies required

---

## Quick Comparison

| Method      | Dependencies | Complexity | Features | Best For |
|-------------|--------------|------------|----------|----------|
| structlog   | ✓            | Medium     | ⭐⭐⭐⭐⭐ | Production apps |
| colorama    | ✓            | Low        | ⭐⭐      | Simple scripts |
| rich        | ✓            | Low        | ⭐⭐⭐⭐⭐ | CLI tools |
| ANSI codes  | ✗            | Low        | ⭐⭐      | Minimal deps |

---

## Running Examples

```bash
# structlog (like cognee)
python examples/colored_logging_structlog.py

# colorama (simple)
python examples/colored_logging_colorama.py

# rich (beautiful)
python examples/colored_logging_rich.py

# ANSI codes (no deps)
python examples/colored_logging_ansi.py
```

---

## Color Reference

### ANSI Colors
- `\033[30m` - Black
- `\033[31m` - Red
- `\033[32m` - Green
- `\033[33m` - Yellow
- `\033[34m` - Blue
- `\033[35m` - Magenta
- `\033[36m` - Cyan
- `\033[37m` - White
- `\033[0m` - Reset

### Rich Markup
- `[red]text[/red]` - Red text
- `[bold]text[/bold]` - Bold
- `[dim]text[/dim]` - Dimmed
- `[green]✓[/green]` - Success
- `[yellow]⚠[/yellow]` - Warning
- `[red]✗[/red]` - Error

---

## How cognee Does It

From the logs you're seeing, cognee uses:

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.dev.ConsoleRenderer(colors=True)
    ],
    # ... more config
)

logger = structlog.get_logger(__name__)
logger.info("Message", key="value", another_key="value2")
```

The colored output is automatic based on log level!
