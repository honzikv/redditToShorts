from dataclasses import dataclass
from datetime import datetime
from typing import List

from reddit_scraper.database.models.comment import Comment


@dataclass
class Post:
    """
    A Reddit post
    """
    _id: str
    title: str
    text: str
    author: str
    comments: List[Comment]
    num_upvotes: int
    date_created: datetime
    processed: bool = False
