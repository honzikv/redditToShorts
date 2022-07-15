from reddit_scraper.database.models.post import Post
from video_editor.director.comment_picker.clip_comment import ClipComment

MAX_CHILD_COMMENTS = 3


def default_comment_picker_algo(post: Post, max_child_comments=MAX_CHILD_COMMENTS):
    """
    Default implementation of the comment picking algorithm. This can be modified if needed
    :param post: post to be processed
    :param max_child_comments: max number of child comments to include in the video
    :return:
    """

    # Main idea is to take the "best" comments from the post and some of their children
    # As a default metric we use upvotes as the score

    # First we sort the comments by score
    sorted_comments = sorted(post.comments, key=lambda comment: comment.num_upvotes, reverse=True)

    # This has some flaws but will work fine in most cases
    # We take the top comments and their children
    picked_comments = []
    for comment in sorted_comments:
        picked_comments.append(ClipComment(  # Root comment
            text=comment.text,
            author=comment.author,
            num_upvotes=comment.num_upvotes,
            children=list(  # child comments
                map(lambda child: ClipComment(  # map them to ClipComment object
                    child.text,
                    child.author,
                    child.num_upvotes
                ),
                    # Pick the most upvoted comments and clamp the number of children to max_child_comments
                    sorted(comment.children, key=lambda child: child.num_upvotes, reverse=True)[:max_child_comments])
            )
        ))

    return picked_comments
