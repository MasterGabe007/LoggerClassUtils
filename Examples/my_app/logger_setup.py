import logging
from pathlib import Path

from shared_logger import Logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = str(PROJECT_ROOT / "logs")
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

logger = Logger(
    name         = "my_app",
    log_file     = "my_app.log",
    level        = logging.INFO,
    log_dir      = LOG_DIR,
    console      = True,
    max_bytes    = 5 * 1024 * 1024,
    backup_count = 5,
    json_logs    = False,
)
