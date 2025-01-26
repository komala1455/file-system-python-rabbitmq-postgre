import pika
from database import get_connection
from models import DataEntry
from config import RABBITMQ_URL, DATA_QUEUE
from logger import logger

def callback(ch, method, properties, body):
    """
    Callback function that processes the message from the RabbitMQ queue.
    
    Args:
        ch: pika channel object that was used to receive the message.
        method: pika method object containing metadata about the message.
        properties: message properties such as content type, delivery mode, etc.
        body: the actual message content, expected to be in JSON format.
    """
    try:
        logger.info("Received message from queue.")
        # Convert message body from JSON string to Python dictionary
        raw_data = body.decode('utf-8').split(',')
        data = {
            'name': raw_data[0],
            'id': int(raw_data[1]),
            'order_id': raw_data[2],
            'order_creation_at': raw_data[3]
        }
        # Open database session
        try:
            db = next(get_connection())

            # Create a new DataEntry object from the message data
            instance = DataEntry(**data)
            # Add the new entry to the database and commit the transaction
            db.add(instance)
            db.commit()
            logger.info(f"Data entry added: {instance}")
        except Exception as e:
            logger.error(f"Error adding data entry to database: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

# Establish connection to RabbitMQ
try:
    logger.info("Connecting to RabbitMQ...")
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    
    # Declare the queue to ensure it exists
    logger.info(f"Declaring queue: {DATA_QUEUE}")
    channel.queue_declare(queue=DATA_QUEUE)
    
    # Set up the consumer
    logger.info("Starting consumer to listen for messages...")
    channel.basic_consume(queue=DATA_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

except Exception as e:
    logger.error(f"Failed to connect to RabbitMQ: {e}")
