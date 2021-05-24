import json
import asyncio
from rctiplus_rabbitmq_python_sdk import AIORabbitMQ, MessagePayload


# Create payload class handler that implement `MessagePayload`
class JSONPayload(MessagePayload):
    """Example class to handle JSON payload
    """

    def __init__(self, firstname: str, lastname: str) -> None:
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self) -> str:
        """Convert JSON to string payload message

        Returns:
            str: String payload message
        """
        return json.dumps({
            'firstname': self.firstname,
            'lastname': self.lastname
        })
    
    @classmethod
    def from_str(cls, message: str) -> 'JSONPayload':
        """Generate data from JSON string payload message

        Returns:
            JSONPayload: Generated data
        """
        payload = json.loads(message)
        return cls(firstname=payload['firstname'], lastname=payload['lastname'])


# Main function
async def main(loop):

    # Connect to RabbitMQ
    conn = AIORabbitMQ(loop)
    await conn.connect(host='localhost', port=5672, username='guest', password='guest')
    
    async with conn.connection:
        # Send payload to queue
        payload = JSONPayload('John', 'Doe')
        print('payload:', payload)
        await conn.send('test', payload)


# Event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()