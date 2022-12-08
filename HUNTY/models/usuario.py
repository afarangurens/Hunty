from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Usuario(BaseModel):
    UserId: Optional[str]
    FirstName: str
    LastName: str
    Email: str
    YearsPreviousExperience: int
    Skills: List[dict] = []
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
