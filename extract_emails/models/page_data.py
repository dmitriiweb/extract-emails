from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class PageData(BaseModel):
    website: str
    page_url: str
    data: Optional[Dict[str, List[str]]] = Field(default_factory=dict)

    def append(self, label: str, vals: List[str]) -> None:
        try:
            self.data[label].extend(vals)
        except KeyError:
            self.data[label] = vals
