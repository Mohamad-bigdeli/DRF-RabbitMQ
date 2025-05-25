import pika
import json 
from django.conf import settings
from pika.exceptions import AMQPConnectionError

class RabbitMQClient:
    
    def __init__(self):
        self.host = settings.RABBITMQ["HOST"]
        self.port = settings.RABBITMQ["PORT"]
        self.virtual_host = settings.RABBITMQ["VIRTUAL_HOST"]
        self.username = settings.RABBITMQ["USERNAME"]
        self.password = settings.RABBITMQ["PASSWORD"]
        self.exchange = settings.RABBITMQ["EXCHANGE"]
        self.exchange_type = settings.RABBITMQ["EXCHANGE_TYPE"]
        self.connection = None
        self.channel = None
        self.is_connected = False
    
    def connect(self) -> None:
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials,
            heartbeat=1200,
            blocked_connection_timeout=300
        )

        try:
            self.connection = pika.BlockingConnection(parameters=parameters)
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)
            self.is_connected = True
            print("Successfully connected to RabbitMQ")
            return
        except AMQPConnectionError as e:
            print(f"Connection attempt failed: {e}\
                  Could not connect to RabbitMQ.")
            raise
    
    def publish_message(self, queue, message, routing_key) -> None:
        if not self.is_connected:
            self.connect()
        try:
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.queue_bind(queue=queue, exchange=self.exchange, routing_key=routing_key)
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_key or queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2) 
            )
            print(f"Message published to queue {queue}: {message}")
        except Exception as e:
            print(f"Failed to publish message: {e}")
            self.is_connected = False
            raise
    
    def consume_message(self, queue, callback, auto_ack=True) -> None:
        if not self.is_connected:
            self.connect()
        try:
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=auto_ack)
            print(f"Starting to consume messages from queue {queue}")
            self.channel.start_consuming()
        except Exception as e:
            print(f"Failed to consume messages: {e}")
            self.is_connected = False
            raise
    
    def close(self) -> None:
        try:
            if self.channel and self.channel.is_open:
                self.channel.close()
            if self.connection and self.connection.is_open:
                self.connection.close()
            self.is_connected = False
            print("RabbitMQ connection closed")
        except Exception as e:
            print(f"Error closing RabbitMQ connection: {e}")
