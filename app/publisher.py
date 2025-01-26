import pika
from config import DATA_QUEUE, RABBITMQ_URL
from logger import logger
import os


class ClientDataEntryPublisher:
    """
    A publisher class for sending client data entries to a RabbitMQ queue.

    Methods
    -------
    __init__():
        Initializes the RabbitMQ connection and declares the queue.

    publish_message(message: str):
        Publishes a message to the RabbitMQ queue.

    close_connection():
        Closes the RabbitMQ connection.

    read_file(file_path: str):
        Reads a file and returns the data as a list of lines.

    push_data(file_path: str):
        Reads client data from a file and publishes each line as a message to the RabbitMQ queue.
    """
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=DATA_QUEUE)

    def publish_message(self, message: str):
        self.channel.basic_publish(exchange='', routing_key=DATA_QUEUE, body=message)
        logger.info(f"Published message: {message}")

    def close_connection(self):
        try:
            self.connection.close()
            logger.info("RabbitMQ connection closed.")
        except Exception as e:
            logger.error(f"Failed to close RabbitMQ connection: {e}")

    def read_file(self, file_path: str):
        # read the file and return the data as a list of lines
        with open(file_path, 'r') as f:
            return f.read().split('\n')

    def push_data(self, file_path: str):
        try:
            clients_data = self.read_file(file_path)
            for data in clients_data:
                logger.info(f"Publishing message: {data}")
                self.publish_message(data)
        except Exception as e:
            logger.error(f"Failed to publish messages: {e}")
            raise
        finally:
            self.close_connection()

try:
    file_path = os.path.join(os.path.dirname(__file__), 'clientdata.txt')
    publisher = ClientDataEntryPublisher()
    publisher.push_data(file_path)
except Exception as e:
    logger.error(f"Failed to publish messages: {e}")
    raise
finally:
    publisher.close_connection()