from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Comment:
    """
    A Reddit comment
    """
    _id: str
    text: str
    author: str  # author name is sufficient for this use-case, could be extended by adding a user object
    date_created: datetime
    num_upvotes: int
    children: List['Comment']
