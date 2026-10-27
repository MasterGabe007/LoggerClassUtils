
# 
# logger_setup.py 
# - Requires:  To import as shown below, it must first be installed as packaged (e.g., pip install "<logger-class-root-path>")
# 
# - Copy this module to the target projects root to initialize the logger_class.py logger for that project.
# 
# - Usage / Integration into app source code:
# 	from logger_setup import logger
# 
# - Usage / Testing:
# 	logger.info("App started...")
# 	logger.debug("Debug message...")
# 

from logger_class import Logger

logger = Logger()
logger.info("Logger initialized successfully.")
