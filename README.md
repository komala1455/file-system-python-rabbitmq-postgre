# File Reader System and Data API

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- PostgreSQL
- Install Docker (https://www.docker.com/products/docker-desktop)
- RabbitMQ

### Installation Steps

1. **Clone the repository**:
   
   git clone https://github.com/komala1455/file-system-python-rabbitmq-postgre.git
   
   cd file-system-python-rabbitmq-postgre

2. **Create and activate a virtual environment**:

   python -m venv file_system
   
   file_system\\Scripts\\activate

3. **Install dependencies**:
  
   pip install -r requirements.txt
   
4. **Set up PostgreSQL database**:

    - Create a new PostgreSQL database.
    - Set the 'POSTGRES_URL' environment variable:
      cmd - export POSTGRES_URL=postgresql://username:password@localhost/dbname

    - Create user using pgAdmin  
    - Create a table using the following SQL command:
      '''
      CREATE TABLE data_table (
          id SERIAL PRIMARY KEY,
          name VARCHAR(255) NOT NULL,
          orderid VARCHAR(255) NOT NULL,
          date DATE NOT NULL
      ); '''

5. **Set up RabbitMQ**:

   - Set the 'RABBITMQ_URL' in environment variable:
     cmd - export RABBITMQ_URL=amqp://guest:guest@localhost/
   - docker pull rabbitmq:3-management
   - docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   - open the rabbitmq application -> **http://localhost:15672/#/queues/%2F/data_queue**


6. **Start the FastAPI server/ Application**:
 
   cd app; python main.py

7. **Start the RabbitMQ Publisher**:

   cd app; python publisher.py

8. **Start the RabbitMQ Consumer**:

   cd app; python consumer.py

9. **API Endpoint**:

   http://localhost:8000/data?name=kom&page=1&size=10


    


