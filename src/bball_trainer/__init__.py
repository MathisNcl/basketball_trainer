import logging

from bball_trainer.schemas.settings import Settings

VERSION = (0, 0, 1)
__version__ = ".".join(map(str, VERSION))

settings = Settings()
logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logger.addHandler(console_handler)
