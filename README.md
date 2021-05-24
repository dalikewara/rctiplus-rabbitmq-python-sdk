# Introduction

A library from RCTI+ to handle RabbitMQ tasks (connect, send, receive, etc) in Python.

# Requirements

- Python >=3.7.3
- Pika ==1.2.0
- Aio-pika ==6.8.0

# Installation

```bash
pip install rctiplus-rabbitmq-python-sdk
```

## Getting latest version

```
pip install rctiplus-rabbitmq-python-sdk --upgrade
```

# Usage

To start using this SDK, you may follow given instructions bellow in order.

## Payload handler

First, you need to create a payload class handler that implement `MessagePayload`. For example, we want to make a class to handle JSON payload:

```python
import json
from rctiplus_rabbitmq_python_sdk import MessagePayload

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
```

`MessagePayload` class from the SDK's core has this functions that require to implemented:

```python
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
```

## Connect to RabbitMQ

Making connection to RabbitMQ server can be done by doing this simple way:

```python
from rctiplus_rabbitmq_python_sdk import RabbitMQ

conn = RabbitMQ()
conn.connect(host='localhost', port=5672, username='guest', password='guest')
```

## Sending message

After you have payload class handler & connected to the RabbitMQ server, now you can try to send a messsage to queue channel. For example, we will send JSON payload message to `test` queue:

```python
payload = JSONPayload('John', 'Doe')
print('payload:', payload)
conn.send('test', payload)
```

## Receiving message

Great. Now, in our consumer app, we want to listen & receive that message, and then doing some stuff:

```python
def callback(ch, method, properties, body):
    print("[x] Received %r" % body)
    data = JSONPayload.from_str(body)
    print(f'data: firstname={data.firstname}, lastname={data.lastname}')

conn.receive('test', callback)
```

## Putting it all together

Here is the complete example from the code above:

```python
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

# Example sender app
# Send payload to queue
payload = JSONPayload('John', 'Doe')
print('payload:', payload)
conn.send('test', payload)

# Example consumer app
# Create a callback to be executed immadiately after recieved a message
def callback(ch, method, properties, body):
    print("[x] Received %r" % body)
    
    # Generate data from string payload message
    data = JSONPayload.from_str(body)
    print(f'data: firstname={data.firstname}, lastname={data.lastname}')

# Receive & listen messages from queue channel
conn.receive('test', callback)
```

# License
GNU General Public License v3