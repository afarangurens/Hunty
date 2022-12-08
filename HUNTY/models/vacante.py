from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Vacante(BaseModel):
    VacancyId: Optional[str]
    PositionName: str
    CompanyName: str
    Salary: int
    Currency: str
    VacancyLink: str
    RequiredSkills: List[dict] = []
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    active: bool = False


