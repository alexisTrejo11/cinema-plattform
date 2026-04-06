"""application logging: NDJSON files + console (see app.hared.core.logging)."""

from app.shared.core.logging import JsonFormatter, setup_logging

__all__ = ["JsonFormatter", "setup_logging"]
