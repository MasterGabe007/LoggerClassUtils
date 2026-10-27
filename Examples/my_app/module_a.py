from my_app.logger_setup import logger


def run_a() -> None:
    logger.info("Module A started", module_name="A")
    logger.warning("Example warning from module A", module_name="A")
