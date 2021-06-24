import asyncio
from rctiplus_rabbitmq_python_sdk import AIORabbitMQ


# Main function
async def main(loop):

    # Connect to RabbitMQ
    conn = AIORabbitMQ(loop)
    await conn.connect(host='localhost', port=5672, username='guest', password='guest')
    
    async with conn.connection:
        # Get queues
        print(await conn.get_list_queues())


# Event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
