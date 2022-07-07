import logging
import os
import time

from dotenv import load_dotenv
from logging import config

from reddit_scraper.conf.logging_conf import logging_conf
from reddit_scraper.database.database import configure_database
from reddit_scraper.posts.posts_repository import post_repository
from reddit_scraper.scraping.reddit_scraper import RedditScraper
from reddit_scraper.scraping.submission_processor import SubmissionProcessor

_logger = logging.getLogger(__name__)


def prepare_start():
    # Load environment variables
    load_dotenv()

    # Configure logging
    config.dictConfig(logging_conf)

    # Parse args
    _logger.info('Parsing subreddits')
    subreddits = os.getenv('subreddits').split(',')

    # Create database
    connection_str = os.getenv('mongoConnectionString')
    database_name = os.getenv('mongoDatabaseName')

    configure_database(connection_str, database_name)

    # Create reddit scraper
    _logger.info('Creating reddit scraper')
    client_id = os.getenv('clientId')
    client_secret = os.getenv('clientSecret')
    user_agent = os.getenv('userAgent')
    username = os.getenv('username')
    reddit_scraper = RedditScraper(client_id, client_secret, user_agent, username)
    _logger.info('Created reddit scraper')

    # Create submission processor
    _logger.info('Creating submission processor')
    submission_processor = SubmissionProcessor(post_repository)

    return subreddits, reddit_scraper, submission_processor


def main():
    _logger.info('Initializing the scraper application')

    # Prepare environment
    subreddits, reddit_scraper, submission_processor = prepare_start()

    _logger.info(f'Subreddits: {subreddits}')

    sleep_interval_secs = int(os.getenv('sleepIntervalSecs'))
    while True:
        # This code runs until the thread is interrupted
        _logger.info('Crawling subreddits...')
        posts = reddit_scraper.scrape_subreddits(subreddits)

        for subreddit, subreddit_posts in posts.items():
            _logger.info(f'Processing subreddit {subreddit}')
            for post_id, post in subreddit_posts.items():
                post = submission_processor.process_submission(post)
                _logger.info(f'Processed post {post_id}')
                _logger.info(f'Saving post: {post_id} to the database')
                try:
                    post_repository.save_post(post)
                except Exception as e:
                    _logger.error(f'Error saving post: {post_id}')
                    _logger.error(e)
            _logger.info(f'Processed subreddit {subreddit}')

        _logger.info('Sleeping for %d seconds', sleep_interval_secs)
        time.sleep(sleep_interval_secs)


if __name__ == '__main__':
    main()
