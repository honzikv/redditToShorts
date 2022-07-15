import logging

from fastapi import FastAPI
from reddit_scraper.conf.prepare_runtime import prepare_runtime

prepare_runtime()
_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = FastAPI()  # Start the application
