from datetime import datetime as dt

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from app.services import ReporteService
from app.utils import rol_requerido

reporte_ns = Namespace("reportes", description="Reportes y estadísticas")
service    = ReporteService()

def validar_fecha(fecha):
    try:
        dt.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


@reporte_ns.route("/ventas")
class ReporteVentas(Resource):

    @jwt_required()
    @rol_requerido("admin")
    @reporte_ns.doc(
        description="Reporte de ventas por rango de fechas",
        params={
            "fecha_inicio": "Fecha inicio YYYY-MM-DD",
            "fecha_fin": "Fecha fin YYYY-MM-DD"
        }
    )
    def get(self):
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_fin = request.args.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return {"error": "Se requieren fecha_inicio y fecha_fin"}, 400
        if not validar_fecha(fecha_inicio) or not validar_fecha(fecha_fin):
            return {"error": "Formato de fecha inválido, use YYYY-MM-DD"}, 400

        return service.ventas_por_rango(fecha_inicio, fecha_fin), 200


@reporte_ns.route("/productos")
class ReporteProductos(Resource):

    @jwt_required()
    @rol_requerido("admin")
    @reporte_ns.doc(
        description="Productos más vendidos",
        params={
            "fecha_inicio": "Fecha inicio YYYY-MM-DD (opcional)",
            "fecha_fin":    "Fecha fin YYYY-MM-DD (opcional)",
            "limite":       "Número de productos a mostrar (default 10)"
        }
    )
    def get(self):
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_fin    = request.args.get("fecha_fin")
        limite       = int(request.args.get("limite", 10))

        if fecha_inicio and not validar_fecha(fecha_inicio):
            return {"error": "Formato de fecha_inicio inválido"}, 400
        if fecha_fin and not validar_fecha(fecha_fin):
            return {"error": "Formato de fecha_fin inválido"}, 400

        return service.productos_mas_vendidos(fecha_inicio, fecha_fin, limite), 200

@reporte_ns.route("/ingresos")
class ReporteIngresos(Resource):

    @jwt_required()
    @rol_requerido("admin")
    @reporte_ns.doc(
        description="Ingresos por periodo",
        params={"periodo": "semana | mes | año"}
    )
    def get(self):
        periodo = request.args.get("periodo", "semana")
        return service.ingresos_por_periodo(periodo), 200