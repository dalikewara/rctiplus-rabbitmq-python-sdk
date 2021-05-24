import urllib.parse
import asyncio
import aio_pika
from rctiplus_rabbitmq_python_sdk import MessagePayload
from typing import Callable

class AIORabbitMQ:

    def __init__(self, loop: asyncio.AbstractEventLoop = None, durable: bool = False,
                 auto_ack: bool = True, auto_delete: bool = False) -> None:
        """Python RabbitMQ library

        Args:
            loop (asyncio.AbstractEventLoop, optional): Event loop (asyncio.get_event_loop() when None). Defaults to None
            durable (bool, optional): Durable mode, prevent from losing messages if RabbitMQ server stops or restarts. Defaults to False
            auto_ack (bool, optional): Auto acknowledgements, remove messages immadiatelly after being received. Defaults to True
            auto_delete (bool, optional): Delete created queue after consumer cancels, disconnects or when channel will be closed. Defaults to False
        """
        self.loop = loop
        self.durable = durable
        self.delivery_mode = None
        if self.durable:
            self.delivery_mode = aio_pika.DeliveryMode(2)  # Make messages persistence if durable mode active
        self.auto_ack = auto_ack
        self.auto_delete = auto_delete
        self.connection = None
        self.channel = None

    async def connect(self, host: str, port: int, username: str, password: str) -> None:
        """Connect to RabbitMQ server

        Args:
            host (str): RabbitMQ host
            port (int): RabbitMQ port
            username (str): RabbitMQ username
            password (str): RabbitMQ password
        """
        username = urllib.parse.quote(username)
        password = urllib.parse.quote(password)
        if port:
            port = ':' + str(port)
        else:
            port = ''
        self.connection = await aio_pika.connect_robust(
            f'amqp://{username}:{password}@{host}{port}/',
            loop=self.loop
        )
        self.channel = await self.connection.channel()

    async def disconnect(self) -> None:
        """Disconnect RabbitMQ connection
        """
        await self.connection.close()

    async def send(self, queue: str, body: MessagePayload, exchange: str = '') -> None:
        """Send message/body to RabbitMQ channel queue

        Args:
            queue (str): Queue name
            body (MessagePayload): Message/body payload
            exchange (str, optional): Exchange name. Defaults to ''
        """
        if exchange == '':
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    bytes(str(body), 'utf-8'),
                    delivery_mode=self.delivery_mode,
                ),
                queue,
            )
        else:
            await self.channel.declare_queue(queue, durable=self.durable, auto_delete=self.auto_delete)
            exchange = await self.channel.declare_exchange(exchange, auto_delete=self.auto_delete)
            await exchange.publish(
                aio_pika.Message(
                    bytes(str(body), 'utf-8'),
                    delivery_mode=self.delivery_mode,
                ),
                queue,
            )

    async def receive(self, queue: str, callback: Callable[
        [
            aio_pika.IncomingMessage
        ], None
    ]) -> None:
        """Listen & receive messages from channel queue

        Args:
            queue (str): Queue name
            callback (Callable[ [ aio_pika.IncomingMessage ], None ]): Callback to be called after receiving a message
        """
        queue = await self.channel.declare_queue(queue, durable=self.durable, auto_delete=self.auto_delete)
        await queue.consume(callback, no_ack=self.auto_ack)

    async def delete_queue(self, queue: str) -> None:
        """Delete channel queue

        Args:
            queue (str): Queue name to be deleted
        """
        await self.channel.queue_delete(queue)
    
    async def delete_exchange(self, exchange: str) -> None:
        """Delete channel exchange

        Args:
            exchange (str): Exchange name to be deleted
        """
        await self.channel.exchange_delete(exchange)

    async def commit_ack(self, incoming_message: aio_pika.IncomingMessage) -> None:
        """Do manual acknowledgements (if `auto_ack` is False), tells RabbitMQ that the message is free to delete.
        Use this inside a callback function

        Args:
            incoming_message (aio_pika.IncomingMessage): `incoming_message` argument from the callback
        """
        await incoming_message.ack()
