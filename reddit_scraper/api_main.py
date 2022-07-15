import logging

from fastapi import FastAPI
from reddit_scraper.conf.prepare_runtime import prepare_runtime
from reddit_scraper.posts.post_controller import posts_router

prepare_runtime()
_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = FastAPI()  # Start the application

    # Include all paths
    app.include_router(posts_router)
