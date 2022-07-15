from dataclasses import dataclass, field
from typing import List


@dataclass
class ClipComment:
    text: str
    author: str
    num_upvotes: int
    children: List['ClipComment'] = field(default_factory=lambda: [])
    total_duration_seconds: float = None
