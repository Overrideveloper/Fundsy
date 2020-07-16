import os
from dotenv import load_dotenv

load_dotenv(".env", override=True)

DATABASE_URI = os.getenv("DATABASE_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
ADMIN_NAME = os.getenv("ADMIN_NAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
AMQP_USERNAME = os.getenv("AMQP_USERNAME")
AMQP_PASSWORD = os.getenv("AMQP_PASSWORD")
AMQP_HOST = os.getenv("AMQP_HOST")
AMQP_PORT = os.getenv("AMQP_PORT")
