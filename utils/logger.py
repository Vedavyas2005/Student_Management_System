import logging
from pathlib import Path
LOG_FILE = Path(__file__).resolve().parent.parent / "app.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def info(msg: str):
    logging.info(msg)

def error(msg: str):
    logging.error(msg)
