# FastAPI File Reader and Data API

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- PostgreSQL
- RabbitMQ

### Installation Steps

1. **Clone the repository**:
   
   git clone <repository-url>
   cd file_system_project

2. **Create and activate a virtual environment**:

   python -m venv file_system
   file_system\\Scripts\\activate

3. **Install dependencies**:
  
  pip install -r requirements.txt

4. **Set up PostgreSQL database**:
    - Create a new PostgreSQL database.
    - Set the 'POSTGRES_URL' environment variable:
      cmd - export POSTGRES_URL=postgresql://username:password@localhost/dbname
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


6. **Start the RabbitMQ consumer**:

   python app/consumer.py

7. **Start the FastAPI server/ Application**:
 
   python main.py

   


    


