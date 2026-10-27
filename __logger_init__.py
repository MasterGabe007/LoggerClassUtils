
# 
# logger class initialization - used to simplify the import of the logger class into new projects
# 
# Usage:
# 	- copy this init file to your project root
#   - then import it into your project source code or main app
#


# imports
import sys
from pathlib import Path

# --- config constants ---
logger_dir = Path.cwd().resolve().parent / "LoggerClassUtils"
app_name   = "app"
log_file   = f"{app_name}.log"



# add the folder containing the 'logger' source code into Python's import path
if logger_dir not in sys.path:
    sys.path.insert(0, logger_dir)

# import the Logger class
from logger_class import Logger


# create the '.\logs\' directory
log_dir = str(Path(__file__).resolve().parent / "logs")
log_dir_path = Path(log_dir)
log_dir_path.mkdir(parents=True, exist_ok=True)

# create Logger instance
logger = Logger(
    name      = app_name,
    log_file  = log_file,
    level     = Logger.Levels.INFO,
    log_dir   = str(log_dir_path),
    console   = True,
    max_bytes = (5 * 1024 * 1024),
    backup_count = 5,
    json_logs = False
)

logger.info("Logger session started", app_name=app_name)
