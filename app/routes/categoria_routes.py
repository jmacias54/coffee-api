# app/routes/categoria_routes.py

from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from flask import request
from app.services.categoria_service import CategoriaService
from app.schemas.categoria_schema import (
    categoria_input_model
)
from app.utils import rol_requerido

categoria_ns = Namespace("categorias", description="Gestión de categorías")
service = CategoriaService()


def serialize_categoria(categoria):
    return {
        "id": categoria.id,
        "nombre": categoria.nombre,
        "descripcion": categoria.descripcion,
        "activo": categoria.activo
    }


@categoria_ns.route("/")
class CategoriaList(Resource):

    @jwt_required()
    @categoria_ns.doc(description="Obtener todas las categorías")
    def get(self):
        categorias = service.obtener_todos()
        return [serialize_categoria(c) for c in categorias], 200

    @jwt_required()
    @rol_requerido("admin")
    @categoria_ns.expect(categoria_input_model(categoria_ns))
    @categoria_ns.doc(description="Crear una nueva categoría")
    def post(self):
        data = request.get_json()
        categoria = service.crear(data)
        return serialize_categoria(categoria), 201


@categoria_ns.route("/<int:id>")
class CategoriaDetalle(Resource):

    @jwt_required()
    @categoria_ns.doc(description="Obtener una categoría por ID")
    def get(self, id):
        categoria = service.obtener_por_id(id)
        return serialize_categoria(categoria), 200

    @jwt_required()
    @rol_requerido("admin")
    @categoria_ns.expect(categoria_input_model(categoria_ns))
    @categoria_ns.doc(description="Actualizar una categoría")
    def put(self, id):
        data = request.get_json()
        categoria = service.actualizar(id, data)
        return serialize_categoria(categoria), 200

    @jwt_required()
    @rol_requerido("admin")
    @categoria_ns.doc(description="Eliminar una categoría (soft delete)")
    def delete(self, id):
        service.eliminar(id)
        return {"mensaje": "Categoría eliminada correctamente"}, 200