import logging
import os
from src.config import Config

os.makedirs("logs", exist_ok=True)
log_file_path = os.path.join("logs", "app.log")

logger = logging.getLogger("UdaPlayLogger")
logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))

if not logger.handlers:
    file_handler = logging.FileHandler(log_file_path)
    file_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_format = logging.Formatter('\033[94m[%(levelname)s]\033[0m %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
