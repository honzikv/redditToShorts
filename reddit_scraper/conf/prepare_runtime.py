
import os
from dotenv import load_dotenv

from reddit_scraper.conf.logging_conf import enable_logging
from reddit_scraper.database.database import configure_database


def prepare_runtime():
    """
    Prepares runtime for the application.
    This includes loading .env files, setting up logging
    and connecting to the Mongo database
    """
    
    # Load .env file
    load_dotenv()
    
    # Configure logging
    enable_logging()
    
    # Configure database
    # Create database
    connection_str = os.getenv('mongoConnectionString')
    database_name = os.getenv('mongoDatabaseName')
    configure_database(connection_str, database_name)
