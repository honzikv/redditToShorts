import logging
from pymongo import MongoClient

_db = None
_logger = logging.getLogger(__name__)


def configure_database(connection_string: str, database_name: str):
    """
    Configures the database - this function should get called once at the beginning of the application
    :param connection_string: connection string
    :param database_name: name of the database
    :return:
    """
    global _db
    if _db is None:
        pass
        _db = MongoClient(connection_string)[database_name]

    _logger.debug(f'Created database instance for database: {database_name}')


def get_database():
    """
    Returns database instance - this needs to be configured before the application is run via configure_database func
    :return:
    """
    return _db
