import os

from dotenv import load_dotenv
from fastapi import FastAPI

from reddit_scraper.database.database import configure_database


def prepare_environment():
    """
    Prepares the environment for the application.
    :return: None
    """
    # Read .env file
    load_dotenv()

    # Create database
    connection_str = os.getenv('mongoConnectionString')
    database_name = os.getenv('mongoDatabaseName')
    configure_database(connection_str, database_name)


if __name__ == "__main__":
    prepare_environment()  # Create the database and load .env values
    app = FastAPI()  # Start the application

