import datetime

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from app.services.corte_service import CorteService
from app.utils import rol_requerido

corte_ns = Namespace("corte", description="Corte de caja")
service  = CorteService()

@corte_ns.route("/hoy")
class CorteHoy(Resource):

    @jwt_required()
    @rol_requerido("admin")
    @corte_ns.doc(description="Corte de caja del día actual")
    def get(self):
        return service.corte_por_fecha(),200


@corte_ns.route("/fecha")
class CortePorFecha(Resource):

    @jwt_required()
    @rol_requerido("admin")
    @corte_ns.doc(description="Corte de caja por fecha específica (admin)",
                  params={"fecha": "Fecha en formato YYYY-MM-DD"})
    def get(self):
        fecha = request.args.get("fecha")
        # valida que venga
        if not fecha:
            return {"error": "Se requiere el parámetro fecha (YYYY-MM-DD)"}, 400

        # valida que tenga el formato correcto
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            return {"error": "Formato de fecha inválido, use YYYY-MM-DD"}, 400


        return service.corte_por_fecha(), 200