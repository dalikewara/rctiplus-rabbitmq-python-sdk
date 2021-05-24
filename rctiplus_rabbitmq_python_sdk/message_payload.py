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
