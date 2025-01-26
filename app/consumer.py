import pika
import json
from database import get_db
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
        data = json.loads(body)
        
        # Open database session
        db = next(get_db())
        
        # Create a new DataEntry object from the message data
        db_entry = DataEntry(name=data['name'], id=data['id'], orderid=data['orderid'], date=data['date'])
        
        # Add the new entry to the database and commit the transaction
        db.add(db_entry)
        db.commit()
        
        logger.info(f"Data entry added: {db_entry}")
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
