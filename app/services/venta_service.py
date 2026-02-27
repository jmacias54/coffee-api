# app/services/venta_service.py
from app.repositories.venta_repo import VentaRepo
from app.repositories.detalle_venta_repo import DetalleVentaRepo
from app.repositories.producto_repo import ProductoRepo
from datetime import datetime
import uuid
from app.database import db

venta_repo    = VentaRepo()
detalle_repo  = DetalleVentaRepo()
producto_repo = ProductoRepo()

class VentaService:

    def obtener_todas(self):
        return venta_repo.obtener_todas()

    def obtener_por_id(self, id):
        venta = venta_repo.obtener_por_id(id)
        if not venta:
            raise ValueError(f"Venta con id {id} no encontrada")
        return venta

    def obtener_ventas_hoy(self):
        return venta_repo.obtener_ventas_hoy()

    def crear(self, data):
        try:
            if not data.get("detalles"):
                raise ValueError("La venta debe tener al menos un producto")

            total = 0
            for item in data["detalles"]:
                producto = producto_repo.obtener_por_id(item["producto_id"])
                if not producto:
                    raise ValueError(f"Producto {item['producto_id']} no encontrado")
                if not producto.activo:
                    raise ValueError(f"Producto {producto.nombre} no disponible")

                item["precio_unit"] = float(producto.precio)
                total += item["precio_unit"] * item["cantidad"]

            pagado_con = float(data["pagado_con"])
            if pagado_con < total:
                raise ValueError("El pago es menor al total")

            folio = f"VTA-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"

            venta = venta_repo.crear({
                "folio": folio,
                "total": total,
                "pagado_con": pagado_con,
                "cambio": round(pagado_con - total, 2),
                "metodo_pago": data.get("metodo_pago", "efectivo"),
                "estado": "cerrada",
                "usuario_id": data["usuario_id"]
            })

            detalle_repo.crear_multiples(data["detalles"], venta.id)

            db.session.commit()
            return venta

        except Exception:
            db.session.rollback()
            raise

    def cancelar(self, id,rol):

        venta = self.obtener_por_id(id)
        if venta.estado == "cancelada":
            raise ValueError("La venta ya está cancelada")

        if rol == "cajero" and venta.creado_en.date() != datetime.utcnow().date():
            raise ValueError("El cajero solo puede cancelar ventas del día")

        return venta_repo.actualizar_estado(id, "cancelada")

    def obtener_resumen_hoy(self):
        ventas = venta_repo.obtener_ventas_hoy()
        total_ventas = len(ventas)
        total_ingresos = sum(
            float(v.total) for v in ventas if v.estado != "cancelada"
        )
        total_canceladas = len(
            [v for v in ventas if v.estado == "cancelada"]
        )

        return {
            "fecha": datetime.utcnow().strftime("%Y-%m-%d"),
            "total_ventas": total_ventas,
            "total_ingresos": round(total_ingresos, 2),
            "total_canceladas": total_canceladas
        }