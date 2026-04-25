"""Correlation ID management using Python contextvars for thread/async safety."""

import uuid
from contextvars import ContextVar
from typing import Optional

# Context variable to store the current request's correlation ID
correlation_id_var: ContextVar[Optional[str]] = ContextVar(
    "correlation_id", default=None
)


def generate_correlation_id() -> str:
    """Generate a new unique correlation ID.

    Returns:
        A UUID4 string suitable for use as a correlation ID.
    """
    return str(uuid.uuid4())


def set_correlation_id(correlation_id: str) -> None:
    """Set the correlation ID for the current execution context.

    Args:
        correlation_id: The correlation ID string to store.
    """
    correlation_id_var.set(correlation_id)


def get_correlation_id() -> Optional[str]:
    """Retrieve the correlation ID for the current execution context.

    Returns:
        The current correlation ID, or None if not set.
    """
    return correlation_id_var.get()


def get_or_create_correlation_id(header_value: Optional[str] = None) -> str:
    """Return an existing correlation ID or create a new one.

    If a header value is provided, it is used as-is. Otherwise a new
    UUID is generated. The result is stored in the context variable.

    Args:
        header_value: Optional correlation ID received from an incoming header.

    Returns:
        The resolved correlation ID.
    """
    correlation_id = header_value if header_value else generate_correlation_id()
    set_correlation_id(correlation_id)
    return correlation_id
