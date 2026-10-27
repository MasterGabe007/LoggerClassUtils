from my_app.logger_setup import logger


def run_b() -> None:
    logger.info("Module B started", module_name="B")
    logger.error("Example error from module B", module_name="B", code="E42")
