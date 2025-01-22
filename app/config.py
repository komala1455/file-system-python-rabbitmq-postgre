import os
from logger import logger

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost/dbname")
DATA_QUEUE = 'data_queue'
TABLE_NAME = 'clients_data'

logger.info(f"Configuration loaded: RABBITMQ_URL={RABBITMQ_URL}, POSTGRES_URL={POSTGRES_URL}, DATA_QUEUE={DATA_QUEUE}, TABLE_NAME={TABLE_NAME}")