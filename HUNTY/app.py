from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from routes.vacante import vacante
from routes.usuario import usuario

app =  FastAPI(
    title="REST API para recomendar vacantes con FastAPI y MongoDB",
    description="Esta es una API en FastAPI para un sistema de recomedación de vacantes.",
    version="0.0.1"
)

app.include_router(vacante)
app.include_router(usuario)

@app.get("/")
def read_root():
    return {"Welcome": "Welcome to my API"}
