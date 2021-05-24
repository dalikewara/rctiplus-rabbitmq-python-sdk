import pika
from rctiplus_rabbitmq_python_sdk import MessagePayload
from typing import Callable

class RabbitMQ:

    def __init__(self, durable: bool = False, auto_ack: bool = True, auto_delete: bool = False) -> None:
        """Python RabbitMQ library

        Args:
            durable (bool, optional): Durable mode, prevent from losing messages if RabbitMQ server stops or restarts. Defaults to False
            auto_ack (bool, optional): Auto acknowledgements, remove messages immadiatelly after being received. Defaults to True
            auto_delete (bool, optional): Delete created queue after consumer cancels or disconnects. Defaults to False
        """
        self.durable = durable
        self.delivery_mode = None
        if self.durable:
            self.delivery_mode = 2 # Make messages persistence if durable mode active
        self.auto_ack = auto_ack
        self.auto_delete = auto_delete
        self.connection = None
        self.channel = None

    def connect(self, host: str, port: int, username: str, password: str) -> None:
        """Connect to RabbitMQ server

        Args:
            host (str): RabbitMQ host
            port (int): RabbitMQ port
            username (str): RabbitMQ username
            password (str): RabbitMQ password
        """
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                credentials=credentials,
            )
        )
        self.channel = self.connection.channel()

    def disconnect(self) -> None:
        """Disconnect RabbitMQ connection
        """
        self.connection.close()

    def send(self, queue: str, body: MessagePayload, exchange: str = '') -> None:
        """Send message/body to RabbitMQ channel queue

        Args:
            queue (str): Queue name
            body (MessagePayload): Message/body payload
            exchange (str, optional): Exchange name. Defaults to ''
        """
        self.channel.queue_declare(queue=queue, durable=self.durable, auto_delete=self.auto_delete)
        self.channel.basic_publish(
            exchange=exchange, routing_key=queue, body=str(body), properties=pika.BasicProperties(
                delivery_mode=self.delivery_mode
            ))

    def receive(self, queue: str, callback: Callable[
        [
            pika.adapters.blocking_connection.BlockingChannel,
            pika.spec.Basic.Deliver,
            pika.spec.BasicProperties,
            bytes
         ], None
    ]) -> None:
        """Listen & receive messages from channel queue

        Args:
            queue (str): Queue name
            callback (Callable[ [ pika.adapters.blocking_connection.BlockingChannel, pika.spec.Basic.Deliver, pika.spec.BasicProperties, bytes ], None ]): Callback to be called after receiving a message
        """
        self.channel.queue_declare(queue=queue, durable=self.durable, auto_delete=self.auto_delete)
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=self.auto_ack)
        self.channel.start_consuming()

    def delete_queue(self, queue: str) -> None:
        """Delete channel queue

        Args:
            queue (str): Queue name to be deleted
        """
        self.channel.queue_delete(queue=queue)
    
    def delete_exchange(self, exchange: str) -> None:
        """Delete channel exchange

        Args:
            exchange (str): Exchange name to be deleted
        """
        self.channel.exchange_delete(exchange=exchange)

    def commit_ack(self, ch: pika.adapters.blocking_connection.BlockingChannel,
                    method: pika.spec.Basic.Deliver) -> None:
        """Do manual acknowledgements (if `auto_ack` is False), tells RabbitMQ that the message is free to delete.
        Use this inside a callback function

        Args:
            ch (pika.adapters.blocking_connection.BlockingChannel): `ch` argument from the callback
            method (pika.spec.Basic.Deliver): `method` argument from the callback
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)
