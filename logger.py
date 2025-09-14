import logging
import os
from datetime import datetime
# Configure logging
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOGS_DIR = os.path.join(os.getcwd(), "logs")
LOGS_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE)

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOGS_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)