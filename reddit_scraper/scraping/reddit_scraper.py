from typing import Dict, List

import praw.models
from praw import Reddit

# List of all available categories
CATEGORIES = ['top', 'hot', 'new', 'controversial', 'rising', ]


class RedditScraper:
    """
    Wrapper for scraping reddit subreddits. This object always scrapes results in form of praw.models.Submission
    objects.
    """

    def __init__(self, client_id: str, client_secret: str, user_agent: str, username: str):
        self._client = Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent,
                              username=username)

        # Functions that return a list of posts for a given category
        self._categories_fns = {
            'top': lambda limit, subreddit: self._client.subreddit(subreddit).top(limit=limit),
            'hot': lambda limit, subreddit: self._client.subreddit(subreddit).hot(limit=limit),
            'new': lambda limit, subreddit: self._client.subreddit(subreddit).new(limit=limit),
            'controversial': lambda limit, subreddit: self._client.subreddit(subreddit).controversial(limit=limit),
            'rising': lambda limit, subreddit: self._client.subreddit(subreddit).rising(limit=limit),
        }

    def scrape_subreddit(self, subreddit: str, categories=CATEGORIES,
                         max_posts_per_category=250) -> Dict[str, praw.models.Submission]:
        """
        Scrapes the requested subreddit
        :param subreddit: subreddit name to scrape
        :param categories: list of categories to scrape - see CATEGORIES for available categories
        :param max_posts_per_category: maximum number of posts to scrape per category - default 250. Note that some
        categories may return fewer posts than this or may have same posts as other categories
        :return: dictionary post.id -> reddit submission
        """
        result = {}  # Dictionary where key is id of post and value is post
        for category in categories:
            if category not in self._categories_fns:
                raise ValueError(f'Category {category} is not supported')

            # Get all the posts from given category
            posts: praw.models.ListingGenerator = self._categories_fns[category](limit=max_posts_per_category,
                                                                                 subreddit=subreddit)
            # Iterate over each post and add it to the dictionary
            for post in posts:
                result[post.id] = post

        # Return the result
        return result

    def scrape_subreddits(self, subreddits: List[str], categories=CATEGORIES,
                          max_posts_per_category=250) -> Dict[str, Dict[str, praw.models.Submission]]:
        """
        Scrapes the requested subreddits
        :param subreddits: list of subreddits to scrape
        :param categories: list of categories to scrape - see CATEGORIES for available categories
        :param max_posts_per_category: maximum number of posts to scrape per category - default 250. Note that some
        categories may return fewer posts than this or may have same posts as other categories
        :return: dictionary subreddit -> dictionary post.id -> reddit submission
        """
        result = {}
        for subreddit in subreddits:
            result[subreddit] = self.scrape_subreddit(subreddit, categories, max_posts_per_category)

        return result
