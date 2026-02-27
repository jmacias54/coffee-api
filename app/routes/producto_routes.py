# app/routes/producto_routes.py
from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import jwt_required
from app.services.producto_service import ProductoService
from app.schemas.producto_schema import producto_model, producto_input_model
from app.utils import rol_requerido

producto_ns = Namespace("productos", description="Gestión de productos")
service = ProductoService()


def producto_a_dict(p):
    return {
        "id": p.id,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "precio": float(p.precio),
        "stock": p.stock,
        "activo": p.activo,
        "imagen_url": p.imagen_url,
        "categoria_id": p.categoria_id
    }


@producto_ns.route("/")
class ProductoList(Resource):

    @jwt_required()
    @producto_ns.doc(description="Obtener todos los productos")
    def get(self):
        productos = service.obtener_todos()
        return [producto_a_dict(p) for p in productos], 200

    @jwt_required()
    @rol_requerido("admin")
    @producto_ns.expect(producto_input_model(producto_ns))
    @producto_ns.doc(description="Crear un nuevo producto")
    def post(self):
        data = request.get_json()
        producto = service.crear(data)
        return producto_a_dict(producto), 201


@producto_ns.route("/<int:id>")
class ProductoDetalle(Resource):

    @jwt_required()
    @producto_ns.doc(description="Obtener un producto por ID")
    def get(self, id):
        producto = service.obtener_por_id(id)
        return producto_a_dict(producto), 200

    @jwt_required()
    @rol_requerido("admin")
    @producto_ns.expect(producto_input_model(producto_ns))
    @producto_ns.doc(description="Actualizar un producto")
    def put(self, id):
        data = request.get_json()
        producto = service.actualizar(id, data)
        return producto_a_dict(producto), 200

    @jwt_required()
    @rol_requerido("admin")
    @producto_ns.doc(description="Eliminar un producto (soft delete)")
    def delete(self, id):
        service.eliminar(id)
        return {"mensaje": "Producto eliminado correctamente"}, 200


@producto_ns.route("/categoria/<int:categoria_id>")
class ProductoPorCategoria(Resource):

    @jwt_required()
    @producto_ns.doc(description="Obtener productos por categoría")
    def get(self, categoria_id):
        productos = service.obtener_por_categoria(categoria_id)
        return [producto_a_dict(p) for p in productos], 200
