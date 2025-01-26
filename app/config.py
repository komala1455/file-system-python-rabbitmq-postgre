import os
from logger import logger

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://komala:komala123@localhost:5432/test_db")

DATA_QUEUE = 'data_queue'
TABLE_NAME = 'orders'

logger.info(f"Configuration loaded: RABBITMQ_URL={RABBITMQ_URL}, POSTGRES_URL={POSTGRES_URL}, DATA_QUEUE={DATA_QUEUE}, TABLE_NAME={TABLE_NAME}")
