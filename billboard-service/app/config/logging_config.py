import logging
from logging.config import dictConfig
import json
from datetime import datetime
from typing import Any, Dict
import os

from app.config.app_config import settings

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
        
        if hasattr(record, 'props'):
            log_record.update(record.props)
            
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)


class AuditSummaryHandler(logging.Handler):
    """Forwards a one-line summary of each audit log record to the app logger (console + file)."""

    def __init__(self, app_logger_name: str = "app", level: int = logging.INFO):
        super().__init__(level=level)
        self._app_logger_name = app_logger_name

    def emit(self, record: logging.LogRecord) -> None:
        try:
            app_logger = logging.getLogger(self._app_logger_name)
            if not app_logger.isEnabledFor(record.levelno):
                return
            props = getattr(record, "props", None) or {}
            msg = record.getMessage()
            # Build a minimal one-line summary
            parts = [msg]
            if "method" in props and "path" in props:
                parts.append(f"{props['method']} {props['path']}")
            if "status_code" in props:
                parts.append(str(props["status_code"]))
            if "process_time" in props:
                t = props["process_time"]
                parts.append(f"{t:.4f}s" if isinstance(t, (int, float)) else str(t))
            if "request_id" in props:
                parts.append(f"id={str(props['request_id'])[:8]}")
            summary = " | ".join(parts)
            app_logger.log(record.levelno, "[audit] %s", summary)
        except Exception:
            self.handleError(record)


def setup_logging():
    debug = getattr(settings, "debug", False)

    console_level = "DEBUG" if debug else "INFO"
    app_level = "DEBUG" if debug else "INFO"

    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "colored": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(bold_white)s%(name)s%(reset)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "log_colors": {
                    'DEBUG': 'cyan',
                    'INFO': 'green', 
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                },
                "secondary_log_colors": {
                    'message': {
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red'
                    }
                },
                "style": "%"
            },
            "json": {
                "()": __name__ + ".JsonFormatter",
            }
        },
        "handlers": {
            "console": {
                "level": console_level,
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
            "audit_file": {
                "level": "INFO",
                "formatter": "json",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/audit_logger.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            }
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file"],
                "level": app_level,
                "propagate": False
            },
            "audit": {
                # Audit logger writes only to file; no console output
                "handlers": ["audit_file"],
                "level": "INFO",
                "propagate": False
            },
            # Uvicorn access log silenced (we handle our own request logs)
            "uvicorn.access": {
                "handlers": [],
                "level": "CRITICAL",
                "propagate": False
            },
            # SQLAlchemy silenced
            "sqlalchemy.engine": {
                "handlers": [],
                "level": "CRITICAL",
                "propagate": False
            },
            "sqlalchemy.dialects": {
                "handlers": [],
                "level": "CRITICAL",
                "propagate": False
            },
            "sqlalchemy.pool": {
                "handlers": [],
                "level": "CRITICAL",
                "propagate": False
            },
            "sqlalchemy.orm": {
                "handlers": [],
                "level": "CRITICAL",
                "propagate": False
            }
        },
    }
    
    os.makedirs("logs", exist_ok=True)
    dictConfig(logging_config)

    # Audit: file-only full log always; console summary only in debug mode
    if debug:
        audit_logger = logging.getLogger("audit")
        audit_logger.addHandler(AuditSummaryHandler(app_logger_name="app", level=logging.INFO))

    sqlalchemy_loggers = ['sqlalchemy.engine','sqlalchemy.dialects', 'sqlalchemy.pool','sqlalchemy.orm']
    
    for logger_name in sqlalchemy_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.CRITICAL)
        
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        logger.propagate = False
      

