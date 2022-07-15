import datetime
import logging
import sys
from typing import Optional, Iterable

import praw.models

from reddit_scraper.database.models.comment import Comment
from reddit_scraper.database.models.post import Post
from reddit_scraper.posts.post_repository import PostRepository

MAX_COMMENTS_PER_SUBMISSION = 250
logger = logging.getLogger(__name__)


class SubmissionProcessor:

    def __init__(self, post_repository: PostRepository):
        self._post_repository = post_repository

    def _map_comments(self, comments: Iterable, max_comments=MAX_COMMENTS_PER_SUBMISSION, fetch_more_comments=False):
        """
        Maps a list of comments from PRAW to a list of Comment objects
        :param fetch_more_comments: max number of comments to fetch - setting this number to zero or below will ignore
        this parameter and fetch all comments
        :param max_comments: max number of comments to map
        :param comments: list of comments
        :return: list of mapped comments
        """

        if max_comments <= 0:
            max_comments = sys.maxsize

        mapped_comments = []
        for comment in comments:
            # First check whether the comment is a MoreComments object
            if isinstance(comment, praw.models.MoreComments):
                if fetch_more_comments:
                    comment.comments(comment.count)
                else:
                    continue

            # Skip any objects that are not an instance of praw.models.Comment
            if not isinstance(comment, praw.models.Comment):
                continue

            # Skip any comments that have no author
            if comment.author is None:
                continue

            logger.debug(f'Mapping comment: {comment.id}')
            mapped_comments.append(
                Comment(
                    _id=comment.id,
                    text=comment.body,
                    # text is stored in markdown so remove all tags
                    author=comment.author.name,
                    # convert from unix timestamp to python datetime
                    date_created=datetime.datetime.fromtimestamp(comment.created_utc),
                    num_upvotes=comment.score,
                    # children are mapped recursively, this could be done more efficiently but it will suffice for now
                    children=self._map_comments(comment.replies)
                ))

        return mapped_comments

    def process_submission(self, submission: praw.models.Submission, max_comments=MAX_COMMENTS_PER_SUBMISSION,
                           fetch_nested_comments=False) -> Optional[Post]:
        """
        Processes passed submission and returns a Post object that can be persisted in the database or None if the post
        cannot be processed
        :return:
        """
        # Filter out any non-text posts or posts that are already in the database
        if not submission.is_self or submission.selftext is None or self._post_repository.post_exists(
                submission.id) or submission.author is None:
            return None

        # Map the comments to a list of Comment objects
        comments = self._map_comments(submission.comments, max_comments, fetch_nested_comments)

        # Create a Post object and return it
        return Post(
            _id=submission.id,
            title=submission.title,
            text=submission.selftext,
            author=submission.author.name,
            date_created=datetime.datetime.fromtimestamp(submission.created_utc),
            num_upvotes=submission.score,
            comments=comments
        )
