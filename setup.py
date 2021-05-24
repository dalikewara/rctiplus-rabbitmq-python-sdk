import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
requirements = [
    'pika==1.2.0',
    'aio-pika==6.8.0'
]
setuptools.setup(
    name="rctiplus-rabbitmq-python-sdk",
    version="1.0.1",
    license="GPLv3",
    author="RCTI+",
    author_email="rctiplus.webmaster@gmail.com",
    url=None,
    description="A library from RCTI+ to handle RabbitMQ tasks (connect, send, receive, etc) in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    keywords=['python', 'rabbitmq', 'rctiplus', 'rcti+', 'sdk'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.3',
    include_package_data=True
)
