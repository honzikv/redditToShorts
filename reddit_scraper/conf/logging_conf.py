# Logger configuration
import logging.config
import logging

logging_conf = {
    "version": 1,
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    },
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        }
    },
    "formatters": {
        "std_out": {
            "format": "[%(asctime)s] %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%d-%m-%Y %I:%M:%S"
        }
    },
}


def enable_logging(conf=logging_conf):
    """
    Configures logging in the application
    """
    logging.config.dictConfig(conf)
    _logger = logging.getLogger(__name__)
    _logger.info('Logging has been enabled.')
