from fastapi import APIRouter, Response, status
from config.db import conn
from schemas.vacante import vacantesEntity, vacanteEntity
from models.vacante import Vacante
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

vacante = APIRouter()

@vacante.get('/vacantes', response_model=list[Vacante], tags=["Vacantes"])
def get_all_vacantes():
    return vacantesEntity(conn.local.vacante.find())

@vacante.post('/vacantes', response_model=Vacante, tags=["Vacantes"])
def create_vacante(vacante: Vacante):
    new_vacante = dict(vacante)
    del new_vacante["VacancyId"]

    id = conn.local.vacante.insert_one(new_vacante).inserted_id
    
    vacante = conn.local.vacante.find_one({"_id": id})

    return vacanteEntity(vacante)


@vacante.get('/vacantes/{id}', response_model=Vacante, tags=["Vacantes"])
def get_vacante(id: str):
    vacante = vacanteEntity(conn.local.vacante.find_one({"_id": ObjectId(id)}))
    
    print(vacante["RequiredSkills"])
    
    return vacante

@vacante.put('/vacantes/{id}', response_model=Vacante, tags=["Vacantes"])
def update_vacante(id: str, vacante: Vacante):
    conn.local.vacante.find_one_and_update({"_id": ObjectId(id)} , {"$set": dict(vacante)})

    return vacanteEntity(conn.local.vacante.find_one({"_id": ObjectId(id)}))

@vacante.delete('/vacantes/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Vacantes"])
def delete_vacante(id: str):
    vacanteEntity(conn.local.vacante.find_one_and_delete({"_id": ObjectId(id)}))

    return Response(status_code=HTTP_204_NO_CONTENT)