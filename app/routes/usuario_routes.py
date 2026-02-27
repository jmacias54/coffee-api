# app/routes/usuario_routes.py
from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import jwt_required
from app.services.usuario_service import UsuarioService
from app.schemas.usuario_schema import usuario_model, usuario_input_model
from app.utils import rol_requerido

usuario_ns = Namespace("usuarios", description="Gestión de usuarios")
service    = UsuarioService()

def usuario_a_dict(u):
    return {
        "id":     u.id,
        "nombre": u.nombre,
        "email":  u.email,
        "rol":    u.rol,
        "activo": u.activo
    }

@usuario_ns.route("/")
class UsuarioList(Resource):

    @jwt_required()
    @usuario_ns.doc(description="Obtener todos los usuarios")
    def get(self):
        usuarios = service.obtener_todos()
        return [usuario_a_dict(u) for u in usuarios], 200

    @jwt_required()
    @rol_requerido("admin")
    @usuario_ns.expect(usuario_input_model(usuario_ns))
    @usuario_ns.doc(description="Crear un nuevo usuario")
    def post(self):
        data = request.get_json()
        usuario = service.crear(data)
        return usuario_a_dict(usuario), 201

@usuario_ns.route("/<int:id>")
class UsuarioDetalle(Resource):

    @jwt_required()
    @rol_requerido("admin")
    @usuario_ns.doc(description="Obtener un usuario por ID")
    def get(self, id):
        usuario = service.obtener_por_id(id)
        return usuario_a_dict(usuario), 200

    @jwt_required()
    @rol_requerido("admin")
    @usuario_ns.expect(usuario_input_model(usuario_ns))
    @usuario_ns.doc(description="Actualizar un usuario")
    def put(self, id):
        data = request.get_json()
        usuario = service.actualizar(id, data)
        return usuario_a_dict(usuario), 200

    @jwt_required()
    @rol_requerido("admin")
    @usuario_ns.doc(description="Eliminar un usuario (soft delete)")
    def delete(self, id):
        service.eliminar(id)
        return {"mensaje": "Usuario eliminado correctamente"}, 200