from fastapi import FastAPI
from routes.usuario import usuario
from routes.vacante import vacante
from config.db import conn
from schemas.vacante import vacantesEntity
from schemas.usuario import usuarioEntity
from models.vacante import Vacante
from bson import ObjectId
from docs import tags_metadata


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

@app.get("/recomendaciones/{UserId}", response_model=list[Vacante], tags=["Recomendaciones"])
def get_recommended_vacantes(id: str):
    usuario = usuarioEntity(conn.local.usuario.find_one({"_id": ObjectId(id)}))
    vacantes = vacantesEntity(conn.local.vacante.find())
    user_skills = usuario["Skills"]
    reccommended_vacantes = []

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
            reccommended_vacantes.append(vacante)
    
    if len(reccommended_vacantes) == 0:
        return "No hay vacantes disponibles para tus habilidades actuales."
    else:
        return reccommended_vacantes
