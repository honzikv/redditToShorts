
class SubredditRepository:
    """
    SubredditRepository is a simple in-memory storage of
    all subreddits to be scraped.
    """

    def __init__(self) -> 'SubredditRepository':
        self._subreddits = set()

    def add_subreddit(self, subreddit: str):
        """
        Adds a subreddit to the list of subreddits to be scraped.
        :param subreddit:
        :return:
        """
        self._subreddits.add(subreddit)

    def get_subreddits(self) -> list:
        """
        Returns the list of subreddits to be scraped.
        :return:
        """
        return self._subreddits

    def add_subreddits(self, subreddits: list):
        """
        Adds a list of subreddits to the list of subreddits to be scraped.
        :param subreddits:
        :return:
        """
        self._subreddits.update(subreddits)

# Singleton instance of subreddit repository
subreddit_repository = SubredditRepository()
