from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Workspace:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    created_at: Optional[datetime] = None