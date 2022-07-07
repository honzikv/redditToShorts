import logging

from fastapi import APIRouter

from reddit_scraper.posts.posts_service import post_service

posts_router = APIRouter(prefix='/posts')
_logger = logging.getLogger(__name__)


@posts_router.get('/')
def get_posts(amount=10):
    """
    Gets the top n newest posts that have processed flag set to false
    :param amount: number of posts to get
    :return: list of posts
    """
    try:
        posts = post_service.get_n_newest_unprocessed_posts(amount)
        return {
            'success': True,
            'message': posts if posts is not None else []
        }
    except Exception as e:
        _logger.error(e)
        return {
            'success': False,
            'message': 'No new posts are available'
        }


@posts_router.put('/{post_id}')
def update_post(post_id: str):
    """
    Marks a post as processed
    :param post_id: The id of the post to mark as processed
    :return:
    """
    try:
        post_service.mark_post_as_processed(post_id)
        return {
            'success': True,
            'message': 'Post successfully updated'
        }
    except Exception as e:
        _logger.error(e)
        return {
            'success': False,
            'message': 'Post could not be updated'
        }


@posts_router.delete('/{post_id}')
def delete_post(post_id: str):
    """
    Deletes a post
    :param post_id: The id of the post to delete
    :return:
    """
    try:
        post_service.delete_post(post_id)
        return {
            'success': True,
            'message': 'Post successfully deleted'
        }
    except Exception as e:
        _logger.error(e)
        return {
            'success': False,
            'message': 'Post could not be deleted'
        }
