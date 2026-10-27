
"""
    logger_class.py
    - (Unified Version) Reusable single-class logger that writes to rotating files and console output.
    
    Author: Gabriel Acosta (MasterGabe)
    
    Logger Features:
     v1 | 2026-08-30
        - writes to both a file and the console
        - is modular for importing into other projects
        - avoids duplicate handlers if you call setup_logger multiple times with the same name
     v2 | 2026-08-30
        - supports rotating log files (based on max_bytes parameter)
        - supports optional JSON structured logs (if json_logs=True)
     v3 | 2026-08-30
        - single-class version of the logger_v2 module (instead of 'setup_logger' factory function)
        - the Logger() class exposses a single object with methods:  info(), warning(), error(), debug(), critical(), and exception()
        - auto-detect caller to use the name and root of the calling source to name the log file and create the logs directory in the same root as caller.
    
    Usage:
        from logger_class import Logger, TraceLevels
        
        logger = setup_logger(
            name         = "my_app",            # optional/auto-detect caller
            log_file     = "my_app.log",        # optional/auto-detect caller
            level        = TraceLevels.INFO,
            console      = True,
            log_dir      = "logs",              # optional/auto-detect caller
            max_bytes    = (5 * 1024 * 1024),   # 5 MB
            backup_count = 5,
            json_logs    = False
        )
        
        logger.info("Application started")
        logger.warning("Warning message", user_id=42, service="demo")
        logger.error("Error message", error_code="E1001")
    
    Install:
        Use command:  pip install -e "<logger-class-root-path>"   to install as a python library module.
"""


import os
import json
import inspect
import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional


class TraceLevels:
    """Log Integer Trace Levels"""
    CRITICAL = 50
    FATAL    = CRITICAL
    ERROR    = 40
    WARNING  = 30
    WARN     = WARNING
    INFO     = 20
    DEBUG    = 10
    NOTSET   = 0

class Logger:
    """Reusable single-class logger that writes to rotating files and console."""
    
    # class level internal members
    _instance    = None
    _initialized = False
    Levels: TraceLevels = TraceLevels
    
    # singleton pattern to return a single-instance on multi-module projects
    def __new__(cls, *args, **kwargs) -> "Logger":
        if cls._instance is None:
            # allocate the memory for the single instance
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @staticmethod
    def _resolve_caller_context() -> tuple[str, str, str]:
        """Detect the caller file and build default logger values from it."""
        for frame_info in inspect.stack()[1:]:
            filename = frame_info.filename
            if filename == __file__:
                continue
            caller_dir = os.path.dirname(os.path.abspath(filename))
            caller_name = os.path.splitext(os.path.basename(filename))[0]
            return caller_dir, caller_name, os.path.join(caller_dir, "logs")
        return os.getcwd(), "app", os.path.join(os.getcwd(), "logs")
    
    # initialization
    def __init__(
        self,
        name: Optional[str]     = None,
        log_file: Optional[str] = None,
        level: int              = TraceLevels.INFO,
        log_dir: Optional[str]  = None,
        console: bool           = True,
        max_bytes: int          = (5 * 1024 * 1024),
        backup_count: int       = 5,
        json_logs: bool         = False,
    ) -> None:
        
        # prevent re-running handler setup when already instantiated
        if Logger._initialized:
            return
        
        # auto-detect caller info for log name and directory
        caller_dir, caller_name, default_logs_dir = self._resolve_caller_context()
        
        if name is None:
            name = caller_name
        if log_file is None:
            log_file = f"{name}.log"
        if log_dir is None:
            log_dir = default_logs_dir
        
        # set members from given args
        self.name         = name
        self.log_file     = log_file
        self.level        = level
        self.log_dir      = os.path.abspath(log_dir)
        self.console      = console
        self.max_bytes    = max_bytes
        self.backup_count = backup_count
        self.json_logs    = json_logs
        
        # create logger object
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # logger formatter - json if enabled or plain text otherwise
        formatter = JSONFormatter() if json_logs else StandardFormatter(
            "%(asctime)s - %(levelname)s - [%(filename)s -> %(funcName)s(), LN:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        
        # file logging - create logs dir and rotating file handler
        if log_file:
            os.makedirs(self.log_dir, exist_ok=True)
            file_path = os.path.join(self.log_dir, os.path.basename(log_file))
            file_handler = RotatingFileHandler(
                file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        # console logging - create stream handler
        if console:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)
        
        # mark initialization as complete
        Logger._initialized = True
    
    # logging methods
    def debug(self, message: str, **kwargs: Any) -> None:
        self.logger.debug(message, extra=kwargs, stacklevel=2)
    
    def info(self, message: str, **kwargs: Any) -> None:
        self.logger.info(message, extra=kwargs, stacklevel=2)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        self.logger.warning(message, extra=kwargs, stacklevel=2)
    
    def error(self, message: str, **kwargs: Any) -> None:
        self.logger.error(message, extra=kwargs, stacklevel=2)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        self.logger.critical(message, extra=kwargs, stacklevel=2)
    
    def exception(self, message: str, **kwargs: Any) -> None:
        self.logger.exception(message, extra=kwargs, stacklevel=2)
    
    def getLogger(self) -> logging.Logger:
        return self.logger
    pass

# plain text string log-record formatter
class StandardFormatter(logging.Formatter):
    """Format log records as plain text, dynamically appending extra kwargs."""
    
    RESERVED_ATTRS = {
        "del", "_del_", "delimiter", "separator", 
        "args", "asctime", "created", "exc_info", "exc_text", "filename", "taskName",
        "funcName", "levelname", "levelno", "lineno", "message", "module",
        "msecs", "msg", "name", "pathname", "process", "processName",
        "relativeCreated", "stack_info", "thread", "threadName",
    }
    
    def format(self, record: logging.LogRecord) -> str:
        # Generate standard formatted string (e.g., "TIMESTAMP - NAME - LEVEL - MESSAGE")
        base_message = super().format(record)
        
        # Extract extra fields passed via extra=kwargs
        extra_fields = []
        delimiter = ",  "
        for key, value in record.__dict__.items():
            if key not in self.RESERVED_ATTRS:
                extra_fields.append(f"{key} = {value}")
            if key in ["del", "_del_", "delimiter", "separator"]:
                delimiter = value  # Allow custom delimiter if provided in extra kwargs"
        
        if record.exc_info:
            extra_fields.append(f"exception={self.formatException(record.exc_info)}")
        
        if record.stack_info:
            extra_fields.append(f"stack_info={self.formatStack(record.stack_info)}")
        
        # Append extra parameters to the end of the log message if present
        if extra_fields:
            if "\n" in delimiter:
                return f"{base_message} {delimiter}" + str(delimiter).join(extra_fields)
            return f"{base_message} | " + str(delimiter).join(extra_fields)
        
        return base_message
    pass

# Json string log-record formatter
class JSONFormatter(logging.Formatter):
    """Format log records as JSON, dynamically appending extra kwargs."""
    
    RESERVED_ATTRS = {
        "del", "_del_", "delimiter", "separator", 
        "args", "asctime", "created", "exc_info", "exc_text", "filename", "taskName",
        "funcName", "levelname", "levelno", "lineno", "message", "module",
        "msecs", "msg", "name", "pathname", "process", "processName",
        "relativeCreated", "stack_info", "thread", "threadName",
    }
    
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "filename": record.filename,      # Real calling file
            "function": record.funcName,      # Real calling function
            "line": record.lineno,            # Real calling line number
            "message": record.getMessage(),
        }
        
        for key, value in record.__dict__.items():
            if key in self.RESERVED_ATTRS:
                continue
            if key not in ("stack_info", "message"):
                payload[key] = value
        
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        
        if record.stack_info:
            payload["stack_info"] = self.formatStack(record.stack_info)
        
        return json.dumps(payload, default=str)
    pass



if __name__ == "__main__":
    logger = Logger(
        name         = "demo_logger",
        log_file     = "demo.log",
        level        = TraceLevels.DEBUG,
        log_dir      = "logs",
        max_bytes    = 1024,
        backup_count = 3,
        json_logs    = False,
    )
    
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message", user_id=42, service="demo")
    logger.error("Error message", error_code="E1001")
