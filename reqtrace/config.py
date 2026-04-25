"""Configuration dataclass for reqtrace middleware."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ReqTraceConfig:
    """Configuration options for the reqtrace middleware.

    Attributes:
        correlation_id_header: HTTP header name used to read/propagate the
            correlation ID. Defaults to ``X-Correlation-ID``.
        expose_header: Whether to include the correlation ID in the response
            headers.
        excluded_paths: List of URL path prefixes that should not be traced
            (e.g. health-check endpoints).
        log_request_body: Whether to include the request body in trace logs.
            Disabled by default for performance and privacy reasons.
    """

    correlation_id_header: str = "X-Correlation-ID"
    expose_header: bool = True
    excluded_paths: List[str] = field(default_factory=lambda: ["/health", "/metrics"])
    log_request_body: bool = False

    def is_excluded(self, path: str) -> bool:
        """Check whether a given request path should be skipped.

        Args:
            path: The URL path of the incoming request.

        Returns:
            True if the path starts with any entry in ``excluded_paths``.
        """
        return any(path.startswith(excluded) for excluded in self.excluded_paths)
