#!/usr/bin/env python3
"""
Run all logging examples to compare output styles
"""
import subprocess
import sys

examples = [
    ("1. ANSI Codes (No dependencies)", "colored_logging_ansi.py"),
    ("2. Colorama (Cross-platform)", "colored_logging_colorama.py"),
    ("3. Structlog (Production-ready)", "colored_logging_structlog.py"),
    ("4. Rich (Beautiful CLI)", "colored_logging_rich.py"),
]

def run_example(title, filename):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")

    try:
        subprocess.run([sys.executable, f"examples/{filename}"], check=True)
    except FileNotFoundError:
        subprocess.run([sys.executable, filename], check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠ Example failed: {e}")
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        sys.exit(0)

    input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("\n🎨 Colored Logging Examples Demo")
    print("Comparing different approaches to terminal colors\n")

    for title, filename in examples:
        try:
            run_example(title, filename)
        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Goodbye!")
            break

    print(f"\n{'='*60}")
    print("✓ Demo complete!")
    print("See examples/README_LOGGING.md for more details")
    print(f"{'='*60}\n")
