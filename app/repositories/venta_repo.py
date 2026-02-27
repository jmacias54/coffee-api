# app/repositories/venta_repo.py
from app.database import db
from app.models.venta import Venta
from datetime import datetime

class VentaRepo:

    def obtener_todas(self):
        return Venta.query.order_by(Venta.creado_en.desc()).all()

    def obtener_por_id(self, id):
        return Venta.query.get(id)

    def obtener_por_folio(self, folio):
        return Venta.query.filter_by(folio=folio).first()

    def obtener_por_fecha(self, fecha):
        return Venta.query.filter(
            db.func.date(Venta.creado_en) == fecha
        ).all()

    def obtener_ventas_hoy(self):
        hoy = datetime.utcnow().date()
        return self.obtener_por_fecha(hoy)

    def crear(self, data):
        venta = Venta(
            folio       = data["folio"],
            total       = data["total"],
            pagado_con  = data["pagado_con"],
            cambio      = data["cambio"],
            metodo_pago = data.get("metodo_pago", "efectivo"),
            estado      = data.get("estado", "abierta"),
            usuario_id  = data["usuario_id"]
        )
        db.session.add(venta)
        return venta

    def actualizar_estado(self, id, estado):
        venta = self.obtener_por_id(id)
        if not venta:
            return None
        venta.estado = estado
        db.session.commit()
        return venta