import logging
import os
from datetime import datetime

os.makedirs('logs', exist_ok=True)

# Get the current date for the log filename
current_date = datetime.now().strftime('%Y-%m-%d')

# Set up logging to log to a file in the 'logs' folder with the current date in the filename
log_filename = f'logs/app_{current_date}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Optional: also log to console
    ]
)
logger = logging.getLogger(__name__)
