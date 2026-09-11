from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Expense:
    id: Optional[int] = None
    amount: float = 0.0
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    date: str = ""
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
