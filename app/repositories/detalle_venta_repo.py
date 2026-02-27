# app/repositories/detalle_venta_repo.py
from app.database import db
from app.models.detalle_venta import DetalleVenta

class DetalleVentaRepo:

    def obtener_por_venta(self, venta_id):
        return DetalleVenta.query.filter_by(venta_id=venta_id).all()

    def crear(self, data):
        detalle = DetalleVenta(
            cantidad    = data["cantidad"],
            precio_unit = data["precio_unit"],
            subtotal    = data["cantidad"] * data["precio_unit"],
            venta_id    = data["venta_id"],
            producto_id = data["producto_id"]
        )
        db.session.add(detalle)
        db.session.commit()
        return detalle

    def crear_multiples(self, detalles, venta_id):
        lista = []
        for item in detalles:
            detalle = DetalleVenta(
                cantidad    = item["cantidad"],
                precio_unit = item["precio_unit"],
                subtotal    = item["cantidad"] * item["precio_unit"],
                venta_id    = venta_id,
                producto_id = item["producto_id"]
            )
            lista.append(detalle)
        db.session.add_all(lista)
        return lista