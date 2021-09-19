from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class PageData(BaseModel):
    website: str
    page_url: str
    data: Optional[Dict[str, List[str]]] = Field(default_factory=dict)
