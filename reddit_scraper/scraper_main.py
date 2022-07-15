import logging
import os
import time

from reddit_scraper.conf.prepare_runtime import prepare_runtime

prepare_runtime()
_logger = logging.getLogger(__name__)

from reddit_scraper.posts.post_repository import post_repository
from reddit_scraper.scraping.reddit_scraper import RedditScraper
from reddit_scraper.scraping.submission_processor import SubmissionProcessor
from reddit_scraper.subreddits.subreddit_service import subreddit_service



def prepare_start():
    # Parse args
    _logger.info('Parsing subreddits')
    subreddit_service.add_subreddits(os.getenv('subreddits').split(','))
    _logger.info('Parsing subreddits complete')

    # Create reddit scraper
    _logger.info('Creating reddit scraper')
    reddit_scraper = RedditScraper(os.getenv('clientId'), os.getenv(
        'clientSecret'), os.getenv('userAgent'), os.getenv('username'))
    _logger.info('Creating reddit scraper complete')

    # Create submission processor
    _logger.info('Creating submission processor')
    submission_processor = SubmissionProcessor(post_repository)

    return reddit_scraper, submission_processor


def main():
    _logger.info('Initializing the scraper application')

    # Prepare environment
    reddit_scraper, submission_processor = prepare_start()
    subreddits = subreddit_service.get_subreddits()

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
                if post is None:
                    continue

                _logger.info(f'Processed post {post_id}')
                _logger.info(f'Saving post: {post_id} to the database')
                try:
                    post_repository.insert_post(post)
                except Exception as e:
                    _logger.error(f'Error saving post: {post_id}')
                    _logger.error(e)
            _logger.info(f'Processed subreddit {subreddit}')

        _logger.info('Sleeping for %d seconds', sleep_interval_secs)
        time.sleep(sleep_interval_secs)


if __name__ == '__main__':
    main()
