import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
setuptools.setup(
    name="rctiplus-rabbitmq-python-sdk",
    version="0.0.1",
    license="GPLv3",
    author="RCTI+",
    author_email="rctiplus.webmaster@gmail.com",
    url="",
    description="A library from RCTI+ to handle RabbitMQ tasks (connect, send, receive, etc) in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    keywords=['python', 'rabbitmq', 'rctiplus', 'rcti+', 'sdk'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.3'
)
