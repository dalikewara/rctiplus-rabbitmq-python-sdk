import json
from rctiplus_rabbitmq_python_sdk import RabbitMQ, MessagePayload

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


# Connect to RabbitMQ
conn = RabbitMQ()
conn.connect(host='localhost', port=5672, username='guest', password='guest')

# Create a callback to be executed immadiately after recieved a message
def callback(ch, method, properties, body):
    print("[x] Received %r" % body)
    
    # Generate data from string payload message
    data = JSONPayload.from_str(body)
    print(f'data: firstname={data.firstname}, lastname={data.lastname}')

# Receive & listen messages from queue channel
conn.receive('test', callback)
