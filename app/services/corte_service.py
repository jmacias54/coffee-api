# app/services/corte_service.py
from app.repositories.venta_repo import VentaRepo
from app.repositories.detalle_venta_repo import DetalleVentaRepo
from datetime import datetime

venta_repo  = VentaRepo()
detalle_repo = DetalleVentaRepo()

class CorteService:

    def corte_por_fecha(self, fecha=None):
        if not fecha:
            fecha = datetime.utcnow().date()
        else:
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

        ventas = venta_repo.obtener_por_fecha(fecha)

        ventas_cerradas   = [v for v in ventas if v.estado == "cerrada"]
        ventas_canceladas = [v for v in ventas if v.estado == "cancelada"]

        total_efectivo = sum(
            float(v.total) for v in ventas_cerradas if v.metodo_pago == "efectivo"
        )
        total_tarjeta = sum(
            float(v.total) for v in ventas_cerradas if v.metodo_pago == "tarjeta"
        )
        total_ingresos = total_efectivo + total_tarjeta

        # productos más vendidos del día
        productos_vendidos = {}
        for venta in ventas_cerradas:
            detalles = detalle_repo.obtener_por_venta(venta.id)
            for detalle in detalles:
                pid = detalle.producto_id
                if pid not in productos_vendidos:
                    productos_vendidos[pid] = {
                        "producto_id": pid,
                        "cantidad":    0,
                        "subtotal":    0
                    }
                productos_vendidos[pid]["cantidad"] += detalle.cantidad
                productos_vendidos[pid]["subtotal"] += float(detalle.subtotal)

        top_productos = sorted(
            productos_vendidos.values(),
            key=lambda x: x["cantidad"],
            reverse=True
        )[:5]

        return {
            "fecha":              str(fecha),
            "total_ventas":       len(ventas_cerradas),
            "total_canceladas":   len(ventas_canceladas),
            "total_efectivo":     round(total_efectivo, 2),
            "total_tarjeta":      round(total_tarjeta, 2),
            "total_ingresos":     round(total_ingresos, 2),
            "top_productos":      top_productos,
            "detalle_ventas":     [{
                "folio":       v.folio,
                "total":       float(v.total),
                "metodo_pago": v.metodo_pago,
                "usuario_id":  v.usuario_id,
                "hora":        v.creado_en.strftime("%H:%M:%S")
            } for v in ventas_cerradas]
        }