from fastapi import APIRouter, Response, status, HTTPException
from config.db import conn
from schemas.usuario import usuarioEntity, usuariosEntity
from models.usuario import Usuario
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

usuario = APIRouter()

@usuario.get('/usuarios', response_model=list[Usuario], tags=["Usuarios"])
def get_all_usuarios():
    usuario = usuariosEntity(conn.local.usuario.find())
    if usuario is not None:
        return usuario
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No hay usuarios en este momento.")

@usuario.post('/usuarios', response_model=Usuario, tags=["Usuarios"])
def create_usuario(usuario: Usuario):
    new_vacante = dict(usuario)
    del new_vacante["UserId"]

    id = conn.local.usuario.insert_one(new_vacante).inserted_id
    if id is not None:
    
        usuario = conn.local.usuario.find_one({"_id": id})

        return usuarioEntity(usuario)
    else:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Hubo un problema con su solicitud.")

@usuario.get('/usuarios/{id}', response_model=Usuario, tags=["Usuarios"])
def get_usuario(id: str):
    usuario = conn.local.usuario.find_one({"_id": ObjectId(id)})
    if usuario is not None:
        usuario = usuarioEntity(usuario)
        return usuario
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Usuario no encontrada.")
    

@usuario.put('/usuarios/{id}', response_model=Usuario, tags=["Usuarios"])
def update_usuario(id: str, usuario: Usuario):
    usuario = conn.local.usuario.find_one_and_update({"_id": ObjectId(id)} , {"$set": dict(usuario)})
    if usuario is not None:
        return usuarioEntity(conn.local.usuario.find_one({"_id": ObjectId(id)}))
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Usuario no encontrada.")

@usuario.delete('/usuarios/{id}',  status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def delete_usuario(id: str):
    usuario = usuarioEntity(conn.local.usuario.find_one_and_delete({"_id": ObjectId(id)}))
    if usuario is not None:
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Usuario no encontrada.")