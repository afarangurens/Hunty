from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from uuid import uuid4 as uuid



class RequiredSkill(BaseModel):
    name: str
    years: int
    
class Vacante(BaseModel):
    VacancyId: Optional[str]
    PositionName: str
    CompanyName: str
    Salary: int
    Currency: str
    VacancyLink: str
    RequiredSkills: List[RequiredSkill] = []
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    active: bool = False


vacantes = []

app =  FastAPI()

@app.get("/")
def read_root():
    return {"Welcome": "Welcome to my API"}

@app.get('/vacantes')
def get_vacante():
    return vacantes
    
@app.post("/vacantes")
def set_vacantes(vacante: Vacante):
    vacante.VacancyId = str(uuid())
    vacantes.append(vacante.dict())
    
    return vacantes[-1]

@app.get("/vacantes/{VacancyId}")
def get_vacante(VacancyId: str):
    for vacante in vacantes:
        if vacante["VacancyId"] == VacancyId:
            return vacante
    raise HTTPException(status_code=404, detail="Vacante no encontrada")


@app.delete("/vacantes/{VacancyId}")
def delete_vacante(VacancyId: str):
    for indx, vacante in enumerate(vacantes):
        if vacante["VacancyId"] == VacancyId:
            vacantes.pop(indx)
            return {"message": "La vacante ha sido borrada exitosamente."}
    raise HTTPException(status_code=404, detail="Vacante no encontrada")