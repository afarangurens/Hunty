from fastapi import APIRouter, Response, status, HTTPException
from config.db import conn
from schemas.vacante import vacantesEntity, vacanteEntity
from models.vacante import Vacante
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

vacante = APIRouter()

@vacante.get('/vacantes', response_model=list[Vacante], tags=["Vacantes"])
def get_all_vacantes():
    vacantes = vacantesEntity(conn.local.vacante.find())
    if vacantes is not None:
        return vacantes
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No hay vacantes en este momento.")

@vacante.post('/vacantes', response_model=Vacante, tags=["Vacantes"])
def create_vacante(vacante: Vacante):
    new_vacante = dict(vacante)
    del new_vacante["VacancyId"]

    id = conn.local.vacante.insert_one(new_vacante).inserted_id
    if id is not None:
        vacante = conn.local.vacante.find_one({"_id": id})

        return vacanteEntity(vacante)
    else:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Hubo un problema con su solicitud.")

@vacante.get('/vacantes/{id}', response_model=Vacante, tags=["Vacantes"])
def get_vacante(id: str):
    vacante = conn.local.vacante.find_one({"_id": ObjectId(id)})
    if vacante is not None:
        vacante = vacanteEntity(vacante)
        return vacante
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Vacante no encontrada.")

@vacante.put('/vacantes/{id}', response_model=Vacante, tags=["Vacantes"])
def update_vacante(id: str, vacante: Vacante):
    vacante = conn.local.vacante.find_one_and_update({"_id": ObjectId(id)} , {"$set": dict(vacante)})

    if vacante is not None:
        return vacanteEntity(conn.local.vacante.find_one({"_id": ObjectId(id)}))
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Vacante no encontrada.")

@vacante.delete('/vacantes/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Vacantes"])
def delete_vacante(id: str):
    vacante = vacanteEntity(conn.local.vacante.find_one_and_delete({"_id": ObjectId(id)}))
    
    if vacante is not None:
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Vacante no encontrada.")
