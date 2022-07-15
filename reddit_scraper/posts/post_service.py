from reddit_scraper.posts.post_repository import post_repository, PostRepository

MAX_POSTS_PER_REQUEST = 10


class PostService:

    def __init__(self, post_repository: PostRepository):
        self._post_repository = post_repository

    def get_n_newest_posts(self, n: int):
        """
        Gets top n newest posts
        :param n:
        :return:
        """
        if n < 0 or n > MAX_POSTS_PER_REQUEST:
            n = MAX_POSTS_PER_REQUEST

        return self._post_repository.get_n_newest_unprocessed_posts(n)

    def delete_post(self, post_id: str):
        """
        Deletes a post
        :param post_id:
        :return:
        """
        self._post_repository.delete_post(post_id)

    def mark_post_as_processed(self, post_id: str):
        """
        Marks a post as processed
        :param post_id:
        :return:
        """
        self._post_repository.mark_post_as_processed(post_id)


post_service = PostService(post_repository)
