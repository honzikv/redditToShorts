from reddit_scraper.subreddits.subreddit_repository import SubredditRepository
from reddit_scraper.subreddits.subreddit_repository import subreddit_repository


class SubredditService:
    """
    Subreddit service for getting and adding subreddits to be scraped.
    """

    def __init__(self, subreddit_repository: SubredditRepository) -> None:
        self._subreddit_repository = subreddit_repository

    def get_subreddits(self) -> list:
        """
        Returns the list of subreddits to be scraped.
        """
        return self._subreddit_repository.get_subreddits()

    def add_subreddit(self, subreddit: str) -> None:
        """
        Adds a subreddit to the list of subreddits to be scraped.
        """
        self._subreddit_repository.add_subreddit(subreddit)

    def add_subreddits(self, subreddits: list) -> None:
        """
        Adds a list of subreddits to the repository
        """
        self._subreddit_repository.add_subreddits(subreddits)


subreddit_service = SubredditService(subreddit_repository)
