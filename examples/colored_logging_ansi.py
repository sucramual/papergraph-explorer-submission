"""
Example: Simple colored output using ANSI escape codes (no dependencies)
"""
from datetime import datetime

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"

def log_info(message, **kwargs):
    timestamp = datetime.now().isoformat()
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"{Colors.CYAN}{timestamp} [info]{Colors.RESET} {message} {Colors.DIM}{context}{Colors.RESET}")

def log_warning(message, **kwargs):
    timestamp = datetime.now().isoformat()
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"{Colors.YELLOW}{timestamp} [warning]{Colors.RESET} {message} {Colors.DIM}{context}{Colors.RESET}")

def log_error(message, **kwargs):
    timestamp = datetime.now().isoformat()
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"{Colors.RED}{timestamp} [error]{Colors.RESET} {message} {Colors.DIM}{context}{Colors.RESET}")

def log_success(message, **kwargs):
    timestamp = datetime.now().isoformat()
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"{Colors.GREEN}{timestamp} [success]{Colors.RESET} {message} {Colors.DIM}{context}{Colors.RESET}")

# Example usage
if __name__ == "__main__":
    print(f"\n{Colors.BOLD}=== Colored Logging Demo ==={Colors.RESET}\n")

    log_info("Database initialized", path="/var/db/cognee.db")
    log_warning("Missing configuration", config_file=".env", using="defaults")
    log_error("Connection failed", host="localhost", port=6333, retry=3)
    log_success("Setup complete", collections=6, vectors=14837)

    # Custom formatting
    print(f"\n{Colors.BOLD}{Colors.CYAN}Custom Styles:{Colors.RESET}")
    print(f"{Colors.GREEN}✓{Colors.RESET} Task completed")
    print(f"{Colors.YELLOW}⚠{Colors.RESET} Warning message")
    print(f"{Colors.RED}✗{Colors.RESET} Error occurred")
    print(f"{Colors.BLUE}ℹ{Colors.RESET} Information")

    # Background colors
    print(f"\n{Colors.BG_GREEN}{Colors.BLACK} SUCCESS {Colors.RESET}")
    print(f"{Colors.BG_YELLOW}{Colors.BLACK} WARNING {Colors.RESET}")
    print(f"{Colors.BG_RED}{Colors.WHITE} ERROR {Colors.RESET}")
