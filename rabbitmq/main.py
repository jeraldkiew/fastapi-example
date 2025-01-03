from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import pika

app = FastAPI()

# RabbitMQ connection details
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "test_queue"

class Message(BaseModel):
    message: str

# Create a connection to RabbitMQ
def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    return connection

# Function to publish a message to RabbitMQ
def publish_message(message: str):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=message)
    connection.close()

# Function to consume messages from RabbitMQ
def consume_messages():
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    def callback(ch, method, properties, body):
        print(f"Received: {body.decode()}")

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()

@app.post("/send/")
async def send_message(payload: Message):
    """
    Endpoint to send a message to RabbitMQ
    """
    publish_message(payload.message)
    return {"status": "Message sent"}

@app.get("/consume/")
async def consume(background_tasks: BackgroundTasks):
    """
    Endpoint to start consuming messages in the background
    """
    background_tasks.add_task(consume_messages)
    return {"status": "Consuming messages in the background"}
