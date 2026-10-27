from my_app.logger_setup import logger
from my_app.module_a import run_a
from my_app.module_b import run_b


def main() -> None:
    logger.info("Application started")
    run_a()
    run_b()
    logger.info("Application finished")


if __name__ == "__main__":
    main()
