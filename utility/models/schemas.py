from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class SystemListBase(BaseModel):
    image_url: str
    name: str
    url: str
    seq: int
    active: bool