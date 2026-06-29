"""
ArthaMind AI — Utility Module
==============================
Shared helpers for logging, timing, formatting, and error handling
used across all modules.
"""

import functools
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from config import LOGS_DIR, settings


# ═══════════════════════════════════════════════════════════════
#  LOGGING
# ═══════════════════════════════════════════════════════════════

def setup_logger(name: str = "arthamind") -> logging.Logger:
    """Create and configure a named logger with file and console handlers.

    Args:
        name: Logger name (used as namespace).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    log_file = LOGS_DIR / f"arthamind_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Default application logger
logger = setup_logger()


# ═══════════════════════════════════════════════════════════════
#  PERFORMANCE
# ═══════════════════════════════════════════════════════════════

def timer(func: Callable) -> Callable:
    """Decorator that logs the execution time of a function.

    Args:
        func: Function to wrap.

    Returns:
        Wrapped function with timing.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.info(f"{func.__name__} completed in {elapsed:.2f}s")
            return result
        except Exception as exc:
            elapsed = time.perf_counter() - start
            logger.error(f"{func.__name__} failed after {elapsed:.2f}s: {exc}")
            raise
    return wrapper


# ═══════════════════════════════════════════════════════════════
#  ERROR HANDLING
# ═══════════════════════════════════════════════════════════════

def safe_execute(func: Callable, *args: Any, default: Any = None, **kwargs: Any) -> Any:
    """Execute a function safely, returning a default on failure.

    Args:
        func: Function to execute.
        *args: Positional arguments.
        default: Value to return on exception.
        **kwargs: Keyword arguments.

    Returns:
        Function result or default value.
    """
    try:
        return func(*args, **kwargs)
    except Exception as exc:
        logger.warning(f"safe_execute caught error in {func.__name__}: {exc}")
        return default


# ═══════════════════════════════════════════════════════════════
#  FORMATTING
# ═══════════════════════════════════════════════════════════════

def format_currency(amount: float, currency: str = "INR", symbol: str = "₹") -> str:
    """Format a number as Indian currency with commas.

    Args:
        amount: Numeric value.
        currency: Currency code (for display).
        symbol: Currency symbol prefix.

    Returns:
        Formatted currency string like ₹12,34,567.89
    """
    if amount < 0:
        return f"-{symbol}{format_indian_number(abs(amount))}"
    return f"{symbol}{format_indian_number(amount)}"


def format_indian_number(number: float) -> str:
    """Format a number using the Indian numbering system (lakhs/crores).

    Args:
        number: Numeric value.

    Returns:
        String with Indian-style comma separators, e.g. 12,34,567.89
    """
    is_negative = number < 0
    number = abs(number)

    integer_part = int(number)
    decimal_part = number - integer_part

    s = str(integer_part)
    if len(s) <= 3:
        formatted = s
    else:
        last_three = s[-3:]
        remaining = s[:-3]
        # Group remaining digits in pairs from right
        groups = []
        while remaining:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        groups.reverse()
        formatted = ",".join(groups) + "," + last_three

    if decimal_part > 0:
        formatted += f".{round(decimal_part * 100):02d}"
    else:
        formatted += ".00"

    return f"-{formatted}" if is_negative else formatted


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format a number as a percentage string.

    Args:
        value: Numeric value (e.g. 8.5 for 8.5%).
        decimals: Decimal places.

    Returns:
        Formatted percentage string.
    """
    return f"{value:.{decimals}f}%"


def format_source_citation(source: str, page: str = "", url: str = "") -> str:
    """Format a source citation for RAG responses.

    Args:
        source: Document name.
        page: Page number or section reference.
        url: Source URL.

    Returns:
        Markdown-formatted citation string.
    """
    parts = [f"📄 **Source:** {source}"]
    if page:
        parts.append(f"📃 **Section:** {page}")
    if url:
        parts.append(f"🔗 **URL:** [{url}]({url})")
    return " | ".join(parts)


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to a maximum length, adding ellipsis if needed.

    Args:
        text: Input text.
        max_length: Maximum character count.

    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


# ═══════════════════════════════════════════════════════════════
#  LANGUAGE
# ═══════════════════════════════════════════════════════════════

def get_language_code(language_name: str) -> str:
    """Convert a language display name to its ISO code.

    Args:
        language_name: Display name (e.g. 'English', 'हिन्दी (Hindi)').

    Returns:
        ISO 639-1 code (e.g. 'en', 'hi'). Defaults to 'en'.
    """
    return settings.SUPPORTED_LANGUAGES.get(language_name, "en")


def get_language_name(code: str) -> str:
    """Convert an ISO language code to its display name.

    Args:
        code: ISO 639-1 code.

    Returns:
        Display name or the code itself if not found.
    """
    for name, lang_code in settings.SUPPORTED_LANGUAGES.items():
        if lang_code == code:
            return name
    return code
