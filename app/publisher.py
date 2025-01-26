import pika
from config import DATA_QUEUE, RABBITMQ_URL
from logger import logger

def publish_message(message: str):
    """
    Publishes a message to a RabbitMQ queue.

    Args:
        message (str): The message to be published.

    Raises:
        pika.exceptions.AMQPError: If there is an issue with the RabbitMQ connection or publishing.
    """
    try:
        logger.info("Establishing connection to RabbitMQ.")
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()

        logger.info(f"Declaring queue: {DATA_QUEUE}.")
        channel.queue_declare(queue=DATA_QUEUE)

        logger.info(f"Publishing message to queue {DATA_QUEUE}: {message}")
        channel.basic_publish(exchange='', routing_key=DATA_QUEUE, body=message)
        logger.info("Message published successfully.")
    except Exception as e:
        logger.error(f"Error publishing message: {e}")
        raise
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()
            logger.info("RabbitMQ connection closed.")
        