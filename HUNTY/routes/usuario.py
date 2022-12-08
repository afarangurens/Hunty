from fastapi import APIRouter, Response
from config.db import conn
from schemas.usuario import usuarioEntity, usuariosEntity
from models.usuario import Usuario
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

usuario = APIRouter()

@usuario.get('/usuarios', response_model=list[Usuario], tags=["Usuarios"])
def get_all_usuarios():
    return usuariosEntity(conn.local.usuario.find())

@usuario.post('/usuarios', response_model=list[Usuario], tags=["Usuarios"])
def create_usuario(usuario: Usuario):
    new_vacante = dict(usuario)
    del new_vacante["UserId"]

    id = conn.local.usuario.insert_one(new_vacante).inserted_id
    
    usuario = conn.local.usuario.find_one({"_id": id})

    return usuarioEntity(usuario)

@usuario.get('/usuarios/{id}', response_model=list[Usuario], tags=["Usuarios"])
def get_usuario(id: str):
    usuario = usuarioEntity(conn.local.usuario.find_one({"_id": ObjectId(id)}))
    
    print(usuario["Skills"])
    
    return usuario

@usuario.put('/usuarios/{id}', response_model=list[Usuario], tags=["Usuarios"])
def update_usuario(id: str, usuario: Usuario):
    conn.local.usuario.find_one_and_update({"_id": ObjectId(id)} , {"$set": dict(usuario)})

    return usuarioEntity(conn.local.usuario.find_one({"_id": ObjectId(id)}))

@usuario.delete('/usuarios/{id}', response_model=list[Usuario], tags=["Usuarios"])
def delete_usuario(id: str):
    usuarioEntity(conn.local.usuario.find_one_and_delete({"_id": ObjectId(id)}))

    return Response(status_code=HTTP_204_NO_CONTENT)