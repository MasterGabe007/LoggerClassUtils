# Logger import and setup methods

This file documents the common ways to reuse a logger across projects and modules.

### Use below command to install as a python library module: 

```powershell
pip install -e "<logger-class-root-path>"
```

**See below for other methods of importing and/or installing.**

---
## Method 1: Simple direct import from a file in the same project

Best when the logger file lives in the project root.

**Folder layout:**

```text
my_app/
├── logger_class.py
├── main.py
├── service.py
└── logs/
```

**`logger_class.py`:**

```python
# logger_class source code parameters sample
class Logger:
    def __init__(
        self,
        name: str = "app",
        log_file: Optional[str] = "app.log",
        level: int = Logger.Levels.INFO,
        log_dir: str = ".",
        console: bool = True,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 5,
        json_logs: bool = False,
    ) -> None:
        ...
```

`main.py`:

```python
from pathlib import Path
from logger_class import Logger
import logging

log_dir = str(Path(__file__).resolve().parent / "logs")
logger  = Logger(name="my_app", log_file="my_app.log", level=Logger.Levels.INFO, log_dir=log_dir, console=True, json_logs=True)
logger.info("App started")
```

This works with plain `from logger_class import Logger` when the file sits in the project root.

No `__init__.py` is required for this direct import pattern.

---
## Method 2: Import from a shared folder using `sys.path`

Useful when the logger file lives outside the project, such as:

```text
\\shared_libs\LoggerClassUtils\logger_class.py
```

`test_app/test.py`:

```python
from pathlib import Path
import sys

logger_dir = r"\\shared_libs\LoggerClassUtils"
if logger_dir not in sys.path:
    sys.path.insert(0, logger_dir)

from logger_class import Logger
import logging

log_dir = str(Path(__file__).resolve().parent / "logs")
Path(log_dir).mkdir(parents=True, exist_ok=True)

logger = Logger(
    name      = "app_trace",
    log_file  = "app_trace.log",
    level     = Logger.Levels.INFO,
    log_dir   = log_dir,
    console   = True,
    json_logs = False,
)

logger.info("Project started")
```

This is simple and does not require `__init__.py` in `test_app`.

---
## Method 3: Package import with `__init__.py`

This is useful when you want a cleaner package-based import:

```text
shared_logger/
├── __init__.py
├── logger_class.py
```

`shared_logger/__init__.py`:

```python
from .logger_class import Logger
```

`shared_logger/logger_class.py`:

```python
# same logger class as above
```

Then add the parent folder to `PYTHONPATH` or install the package.
Use below command to install as a python library module.

Example:
```powershell
pip install -e "<logger-class-root-path>"
```

```powershell
set PYTHONPATH=\\shared_libs\LoggerClassUtils;%PYTHONPATH%
```

Then in any app:

```python
from shared_logger import Logger
```

This requires `__init__.py` because it is now a package.


---
## Method 4: Recommended project pattern for real apps

Use a project-local logger setup file so you do not repeat setup code everywhere.

Folder layout:

```text
my_project/
├── logger_setup.py
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── module_a.py
│   └── module_b.py
└── logs/
```

`logger_setup.py`:

```python
from logger_class import Logger
import logging
from pathlib import Path

log_dir = Path(__file__).resolve().parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logger = Logger(
    name      = "my_project",
    log_file  = "my_project.log",
    level     = Logger.Levels.INFO,
    log_dir   = str(log_dir),
    console   = True,
    json_logs = False,
)
```

`app/module_a.py`:

```python
from my_project.logger_setup import logger

logger.info("module_a started")
```

`app/main.py`:

```python
from my_project.logger_setup import logger

logger.info("main started")
```

This is the cleanest pattern for larger projects.

---

## Recommendation

If you want the shortest possible code in each app:

- put `logger_class.py` in the project root, or
- add a shared folder to `PYTHONPATH`, and
- then import with:

```python
from logger_class import Logger
```

No `__init__.py` is needed if you are importing a single module file directly.

If you want package-style imports, then use `__init__.py` and import from the package instead.

---

## Summary

- Direct import: `from logger_class import Logger` -> no `__init__.py` required
- Shared folder import: add folder to `sys.path` or `PYTHONPATH`
- Package import: use `__init__.py` and import from the package
- Best project pattern: one `logger_setup.py` file plus one shared logger module
