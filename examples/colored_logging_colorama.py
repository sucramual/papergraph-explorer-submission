"""
Example: Simple colored output using colorama
"""
from colorama import Fore, Back, Style, init
from datetime import datetime

# Initialize colorama
init(autoreset=True)

def log_info(message, **kwargs):
    timestamp = datetime.now().isoformat()
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"{Fore.CYAN}{timestamp} [info] {message} {Style.DIM}{context}{Style.RESET_ALL}")

def log_warning(message, **kwargs):
    timestamp = datetime.now().isoformat()
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"{Fore.YELLOW}{timestamp} [warning] {message} {Style.DIM}{context}{Style.RESET_ALL}")

def log_error(message, **kwargs):
    timestamp = datetime.now().isoformat()
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"{Fore.RED}{timestamp} [error] {message} {Style.DIM}{context}{Style.RESET_ALL}")

def log_success(message, **kwargs):
    timestamp = datetime.now().isoformat()
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"{Fore.GREEN}{timestamp} [success] {message} {Style.DIM}{context}{Style.RESET_ALL}")

# Example usage
if __name__ == "__main__":
    log_info("Database connected", host="localhost", port=5432)
    log_warning("Using default config", file=".env.example")
    log_error("Connection timeout", retry=3, elapsed="5.2s")
    log_success("Setup complete", collections=6, vectors=14837)

    # Custom colors
    print(f"\n{Fore.MAGENTA}Custom colored output{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}Background colors{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}Bold text{Style.RESET_ALL}")
