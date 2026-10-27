# LoggerClassUtils

Reusable logger module for Python projects.

Install in editable mode:

```powershell
python -m pip install -e "<path_to_logger_dir>\LoggerClassUtils"
```

Then import:

```python
from logger_class import Logger
```

Source-tree package usage:

```python
from LoggerClassUtils import Logger
```

See `README_Logger_Import_Methods.md_` for additional examples of other methods of importing the logger_class utility.

---


## Core Features
- Single-Class API: A simple Logger class with methods like debug(), info(), warning(), error(), critical(), and exception().
- Singleton Pattern: Only one instance of the logger is created across your application, even if instantiated multiple times.
- Auto-Context Detection: Automatically infers the caller's module name, directory, and creates a logs/ folder based off of it if no values are provided.
- Dual Output: Logs to both a rotating log file and the console simultaneously. The console can be toggled with the console parameter.

## Logging & Rotation
- Multiple Log Levels: Supports all standard levels via the TraceLevels class (CRITICAL/FATAL, ERROR, WARNING/WARN, INFO, DEBUG, and NOTSET).
- Size-Based Log Rotation: Uses RotatingFileHandler to automatically rotate logs based off of max_bytes with a configurable backup_count.
- UTF-8 Support: All log files are written with UTF-8 encoding.
- Non-Propagating Logs: The logger has propagate = False to prevent duplicate logs from reaching the root logger.

## Formatting & Extensibility
- Plain Text Formatting: The StandardFormatter includes timestamps, log level, filename, function name, line number, and your message.
- Structured JSON Logging: Enable with json_logs=True to output logs as JSON, including timestamps, logger name, caller context, message, and any extra fields.
- Arbitrary Metadata: Pass key-value pairs to any log method (e.g., logger.info("msg", user_id=42)) and they'll be appended to your logs.
- Exception & Stack Trace Support: The exception() method and automatic inclusion of exc_info and stack_info in both formatters.
- Custom Delimiters: Customize how extra fields are separated via del, delimiter, or separator kwargs.

## Configuration & Safety
- Highly Configurable: Customize with name, log_file, level, log_dir, console, max_bytes, backup_count, and json_logs.
- Automatic Directory Creation: The log directory is created if it doesn't already exist.
- Duplicate Handler Prevention: Existing handlers are cleared on initialization and re-instantiation is safely ignored to prevent duplicate logs.

---
