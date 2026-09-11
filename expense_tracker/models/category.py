from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    id: Optional[int] = None
    name: str = ""
