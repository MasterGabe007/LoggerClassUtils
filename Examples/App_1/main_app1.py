
# below import requires the logger to be installed as packaged (e.g., pip install "<logger-class-root-path>")
from logger_class import Logger

logger = Logger()
logger.info('hello from caller auto detection')
logger.info('hello from caller given at runtime', caller='main_app_custom_name')
