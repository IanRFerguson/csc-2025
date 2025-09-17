import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger("data_engineering_logger")

if os.environ.get("DEBUG", "false").lower() == "true":
    logger.setLevel(logging.DEBUG)
    logger.debug("** Debugger Active **")
