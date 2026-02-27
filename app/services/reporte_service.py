# app/services/reporte_service.py
from app.repositories.venta_repo import VentaRepo
from app.repositories.detalle_venta_repo import DetalleVentaRepo
from app.repositories.producto_repo import ProductoRepo
from datetime import datetime, timedelta

venta_repo   = VentaRepo()
detalle_repo = DetalleVentaRepo()
producto_repo = ProductoRepo()

class ReporteService:

    def ventas_por_rango(self, fecha_inicio, fecha_fin):
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin    = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        if fecha_inicio > fecha_fin:
            raise ValueError("La fecha inicio no puede ser mayor a la fecha fin")

        # obtener ventas día por día
        resultado = []
        fecha_actual = fecha_inicio
        total_general = 0

        while fecha_actual <= fecha_fin:
            ventas = venta_repo.obtener_por_fecha(fecha_actual)
            ventas_cerradas = [v for v in ventas if v.estado == "cerrada"]
            total_dia = sum(float(v.total) for v in ventas_cerradas)
            total_general += total_dia

            resultado.append({
                "fecha":        str(fecha_actual),
                "total_ventas": len(ventas_cerradas),
                "total":        round(total_dia, 2)
            })
            fecha_actual += timedelta(days=1)

        return {
            "fecha_inicio":   str(fecha_inicio),
            "fecha_fin":      str(fecha_fin),
            "total_general":  round(total_general, 2),
            "dias":           resultado
        }

    def productos_mas_vendidos(self, fecha_inicio=None, fecha_fin=None, limite=10):
        if fecha_inicio and fecha_fin:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin    = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        else:
            # por defecto último mes
            fecha_fin    = datetime.utcnow().date()
            fecha_inicio = fecha_fin - timedelta(days=30)

        # obtener todas las ventas del rango
        productos_vendidos = {}
        fecha_actual = fecha_inicio

        while fecha_actual <= fecha_fin:
            ventas = venta_repo.obtener_por_fecha(fecha_actual)
            for venta in ventas:
                if venta.estado == "cancelada":
                    continue
                detalles = detalle_repo.obtener_por_venta(venta.id)
                for detalle in detalles:
                    pid = detalle.producto_id
                    if pid not in productos_vendidos:
                        producto = producto_repo.obtener_por_id(pid)
                        productos_vendidos[pid] = {
                            "producto_id": pid,
                            "nombre":      producto.nombre if producto else "Desconocido",
                            "cantidad":    0,
                            "total":       0
                        }
                    productos_vendidos[pid]["cantidad"] += detalle.cantidad
                    productos_vendidos[pid]["total"]    += float(detalle.subtotal)
            fecha_actual += timedelta(days=1)

        top = sorted(
            productos_vendidos.values(),
            key=lambda x: x["cantidad"],
            reverse=True
        )[:limite]

        # redondea totales
        for p in top:
            p["total"] = round(p["total"], 2)

        return {
            "fecha_inicio": str(fecha_inicio),
            "fecha_fin":    str(fecha_fin),
            "productos":    top
        }

    def ingresos_por_periodo(self, periodo="semana"):
        hoy = datetime.utcnow().date()

        if periodo == "semana":
            fecha_inicio = hoy - timedelta(days=7)
        elif periodo == "mes":
            fecha_inicio = hoy - timedelta(days=30)
        elif periodo == "año":
            fecha_inicio = hoy - timedelta(days=365)
        else:
            raise ValueError("Periodo inválido. Use: semana, mes, año")

        resultado = self.ventas_por_rango(
            str(fecha_inicio),
            str(hoy)
        )
        resultado["periodo"] = periodo
        return resultado