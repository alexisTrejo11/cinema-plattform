import json
import logging
import os
from datetime import datetime, timezone
from logging.config import dictConfig
from typing import Any, Dict, Optional


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class JsonFormatter(logging.Formatter):
    """One JSON object per line (NDJSON), suitable for log shippers and ELK."""

    def __init__(self, *args, service: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._service = service or os.environ.get("SERVICE_NAME", "concession-service")

    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "@timestamp": _utc_now_iso(),
            "timestamp": _utc_now_iso(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "service": self._service,
            "environment": os.environ.get(
                "ENVIRONMENT", os.environ.get("ENV", "development")
            ),
        }

        if hasattr(record, "props"):
            log_record.update(record.props)

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record, default=str)


def setup_logging() -> None:
    log_dir = os.environ.get("LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)

    app_log_path = os.path.join(log_dir, "app.log")
    audit_log_path = os.path.join(log_dir, "audit.log")

    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "colored": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(bold_white)s%(name)s%(reset)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
                "secondary_log_colors": {
                    "message": {"ERROR": "red", "CRITICAL": "bold_red"}
                },
                "style": "%",
            },
            "json_app": {
                "()": JsonFormatter,
            },
            "json_audit": {
                "()": JsonFormatter,
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "formatter": "colored",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "app_file": {
                "level": "DEBUG",
                "formatter": "json_app",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": app_log_path,
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf-8",
            },
            "audit_file": {
                "level": "INFO",
                "formatter": "json_audit",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": audit_log_path,
                "maxBytes": 10485760,
                "backupCount": 10,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console", "app_file"],
                "level": "INFO",
                "propagate": False,
            },
            "audit": {
                "handlers": ["audit_file"],
                "level": "INFO",
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": [],
                "level": "CRITICAL",
                "propagate": False,
            },
            "sqlalchemy.dialects": {
                "handlers": [],
                "level": "CRITICAL",
                "propagate": False,
            },
            "sqlalchemy.pool": {
                "handlers": [],
                "level": "CRITICAL",
                "propagate": False,
            },
            "sqlalchemy.orm": {"handlers": [], "level": "CRITICAL", "propagate": False},
        },
    }

    dictConfig(logging_config)

    sqlalchemy_loggers = [
        "sqlalchemy.engine",
        "sqlalchemy.dialects",
        "sqlalchemy.pool",
        "sqlalchemy.orm",
    ]

    for logger_name in sqlalchemy_loggers:
        sa_logger = logging.getLogger(logger_name)
        sa_logger.setLevel(logging.CRITICAL)

        for handler in sa_logger.handlers[:]:
            sa_logger.removeHandler(handler)

        sa_logger.propagate = False
