import logging
from logging.config import dictConfig
import json
from datetime import datetime
from typing import Any, Dict
import os


class JsonFormatter(logging.Formatter):
    def format(self, record: Any):
        log_record: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "props"):
            log_record.update(record.props)

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logging():
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
            "json": {
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
            "file": {
                "level": "DEBUG",
                "formatter": "json",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "audit": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            # SQLAlchemy silenced
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

    os.makedirs("logs", exist_ok=True)
    dictConfig(logging_config)

    sqlalchemy_loggers = [
        "sqlalchemy.engine",
        "sqlalchemy.dialects",
        "sqlalchemy.pool",
        "sqlalchemy.orm",
    ]

    for logger_name in sqlalchemy_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.CRITICAL)

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        logger.propagate = False
