import dataclasses

from reddit_scraper.database.database import get_database
from reddit_scraper.database.models.post import Post


class PostRepository:

    @property
    def _posts(self):
        return get_database().posts

    def insert_post(self, post: Post):
        """
        Inserts a post
        :param post:
        :return:
        """
        self._posts.insert_one(dataclasses.asdict(post))

    def find_post_by_id(self, post_id: str):
        """
        Finds a post by its id
        :param post_id:
        :return:
        """
        return self._posts.find_one({'_id': post_id})

    def post_exists(self, post_id: str):
        """
        Checks if a post with the given id exists in the database
        :param post_id: The id of the post to check
        :return: True if the post exists, False otherwise
        """
        return self._posts.find_one({'_id': post_id}) is not None

    def get_n_newest_unprocessed_posts(self, n: int):
        """
        Gets top n newest posts that have processed flag set to false
        :param n: number of posts to get
        :return: list of posts
        """
        return self._posts.find({'processed': False}).sort('date_created', -1).limit(n)

    def delete_post(self, post_id: str):
        """
        Deletes a post
        :param post_id:
        :return:
        """
        self._posts.delete_one({'_id': post_id})

    def mark_post_as_processed(self, post_id):
        """
        Marks a post as processed
        :param post_id:
        :return:
        """
        self._posts.update_one({'_id': post_id}, {'$set': {'processed': True}})


# Singleton instance of post repository
post_repository = PostRepository()
