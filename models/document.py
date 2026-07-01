from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Document:
    id: Optional[int] = None
    workspace_id: int = 0

    file_name: str = ""
    file_type: str = ""
    file_path: str = ""

    file_size: int = 0
    status: str = "uploaded"

    extracted_text: str = ""

    created_at: Optional[datetime] = None