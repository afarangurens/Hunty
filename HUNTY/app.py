from fastapi import FastAPI, HTTPException
from routes.usuario import usuario
from routes.vacante import vacante
from config.db import conn
from schemas.vacante import vacantesEntity
from schemas.usuario import usuarioEntity
from models.vacante import Vacante
from bson import ObjectId
from docs import tags_metadata
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

app =  FastAPI(
    title="REST API para recomendar vacantes con FastAPI y MongoDB",
    description="Esta es una API en FastAPI para un sistema de recomedación de vacantes.",
    version="0.0.1",
    openapi_tags=tags_metadata
)

app.include_router(vacante)
app.include_router(usuario)

@app.get("/")
def read_root():
    return {"Welcome": "Welcome to my API"}

@app.get("/recomendaciones/{id}", tags=["Recomendaciones"])
def get_recommended_vacantes(id: str):
    usuario = conn.local.usuario.find_one({"_id": ObjectId(id)})
    if usuario is not None:
        usuario = usuarioEntity(usuario)
        print("helo=?")
        vacantes = vacantesEntity(conn.local.vacante.find())
        if vacantes is not None:
            print("arewwe")
            user_skills = usuario["Skills"]
            recommended_vacantes = []

            for vacante in vacantes:
                vacante_skills = vacante["RequiredSkills"]

                number_of_skills = len(vacante_skills)

                approved_skills = 0

                if user_skills == [] or vacante_skills == []: continue
                
                for skill in user_skills:
                    for skill2 in vacante_skills:
                        if skill.keys() == skill2.keys():     
                            if list(skill.items())[0][1] >= list(skill2.items())[0][1]:
                                approved_skills += 1
                
                if approved_skills >= number_of_skills * 0.5:
                    recommended_vacantes.append(vacante)
            
            if recommended_vacantes is not []:
                return recommended_vacantes
        else:
            return HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No existe esa vacante")
    else:
        return HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No existe el usuario.")