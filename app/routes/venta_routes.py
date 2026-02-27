# app/routes/venta_routes.py
import json

from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.venta_service import VentaService
from app.schemas.venta_schema import venta_model, venta_input_model
from app.utils import rol_requerido

venta_ns = Namespace("ventas", description="Gestión de ventas")
service  = VentaService()

def venta_a_dict(v):
    return {
        "id":          v.id,
        "folio":       v.folio,
        "total":       float(v.total),
        "pagado_con":  float(v.pagado_con),
        "cambio":      float(v.cambio),
        "metodo_pago": v.metodo_pago,
        "estado":      v.estado,
        "usuario_id":  v.usuario_id,
        "creado_en":   v.creado_en.strftime("%Y-%m-%d %H:%M:%S")
    }

@venta_ns.route("/")
class VentaList(Resource):

    @jwt_required()
    @rol_requerido("admin")
    @venta_ns.doc(description="Obtener todas las ventas")
    def get(self):
        ventas = service.obtener_todas()
        return [venta_a_dict(v) for v in ventas], 200

    @jwt_required()
    @rol_requerido("admin")
    @venta_ns.expect(venta_input_model(venta_ns))
    @venta_ns.doc(description="Registrar una nueva venta")
    def post(self):
        data = request.get_json()
        venta = service.crear(data)
        return venta_a_dict(venta), 201

@venta_ns.route("/<int:id>")
class VentaDetalle(Resource):

    @jwt_required()
    @rol_requerido("admin")
    @venta_ns.doc(description="Obtener una venta por ID")
    def get(self, id):
        venta = service.obtener_por_id(id)
        return venta_a_dict(venta), 200

@venta_ns.route("/<int:id>/cancelar")
class VentaCancelar(Resource):

    @jwt_required()
    @rol_requerido("admin", "cajero")
    @venta_ns.doc(description="Cancelar una venta")
    def put(self, id):
        identity = json.loads(get_jwt_identity())
        venta = service.cancelar(id, identity["rol"])
        return venta_a_dict(venta), 200

@venta_ns.route("/hoy")
class VentasHoy(Resource):

    @jwt_required()
    @rol_requerido("admin")
    @venta_ns.doc(description="Obtener resumen de ventas del día")
    def get(self):
        return service.obtener_resumen_hoy(), 200