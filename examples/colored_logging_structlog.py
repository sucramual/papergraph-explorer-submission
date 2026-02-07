"""
Example: Colored logging with structlog (same as cognee uses)
"""
import structlog
import logging

# Configure structlog with colored output
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.dev.ConsoleRenderer(colors=True)  # Enable colors
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)

logger = structlog.get_logger()

# Example usage
if __name__ == "__main__":
    logger.info("Application started", version="1.0.0", environment="production")
    logger.warning("Configuration missing", config_file=".env", action="using_defaults")
    logger.error("Database connection failed", host="localhost", port=5432, retry_count=3)

    # With key-value context
    logger.info(
        "Processing invoice",
        invoice_id="INV-001",
        vendor="TechSupply",
        amount=60000,
        status="completed"
    )

    logger.debug("Debug information", module="setup.py", function="main")
