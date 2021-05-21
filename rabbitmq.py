import pika
from typing import Callable

class RabbitMQ:

    def __init__(self, durable: bool = False, auto_ack: bool = True) -> None:
        """Python RabbitMQ library

        Args:
            durable (bool, optional): Durable mode, prevent from losing messages if RabbitMQ server stops or restarts. Defaults to False
            auto_ack (bool, optional): Auto acknowledgements, remove messages immadiatelly after being received. Defaults to True.
        """
        self.durable = durable
        self.delivery_mode = None
        if self.durable:
            self.delivery_mode = 2 # Make messages persistence if durable mode active
        self.auto_ack = auto_ack
        self.conn = None
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
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                credentials=credentials,
            )
        )
        self.channel = self.conn.channel()

    def disconnect(self) -> None:
        """Disconnect RabbitMQ connection
        """
        self.conn.close()

    def send(self, queue: str, body: 'MessagePayload') -> None:
        """Send message/body to RabbitMQ channel queue

        Args:
            queue (str): Queue name
            body (MessagePayload): Message/body payload
        """
        self.channel.queue_declare(queue=queue, durable=self.durable)
        self.channel.basic_publish(
            exchange='', routing_key=queue, body=str(body), properties=pika.BasicProperties(
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
        self.channel.queue_declare(queue=queue, durable=self.durable)
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=self.auto_ack)
        self.channel.start_consuming()

    def delete_queue(self, queue: str) -> None:
        """Delete channel queue

        Args:
            queue (str): Queue name to be deleted
        """
        self.channel.queue_delete(queue=queue)

    def commit_ack(self, ch: pika.adapters.blocking_connection.BlockingChannel,
                    method: pika.spec.Basic.Deliver) -> None:
        """Do manual acknowledgements (if `auto_ack` is False), tells RabbitMQ that the message is free to delete.
        Use this inside a callback function

        Args:
            ch (pika.adapters.blocking_connection.BlockingChannel): `ch` argument from the callback
            method (pika.spec.Basic.Deliver): `method` argument from the callback
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)


class MessagePayload:
    """Python RabbitMQ message payload
    """
    
    @classmethod
    def from_str(cls, message: str) -> 'MessagePayload':
        """Generate data from specified string payload message format

        Raises:
            NotImplementedError: Raise an error if not implemented
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        """Convert specified data format to string payload message

        Raises:
            NotImplementedError: Raise an error if not implemented

        Returns:
            str: String payload message
        """
        raise NotImplementedError()
