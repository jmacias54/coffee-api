# app/models/venta.py
from app.database import db
from datetime import datetime

class Venta(db.Model):
    __tablename__ = "ventas"

    id          = db.Column(db.Integer, primary_key=True)
    folio       = db.Column(db.String(20), nullable=False, unique=True)
    total       = db.Column(db.Numeric(10, 2), nullable=False)
    pagado_con  = db.Column(db.Numeric(10, 2), nullable=False)
    cambio      = db.Column(db.Numeric(10, 2), nullable=False)
    metodo_pago = db.Column(db.Enum("efectivo", "tarjeta", name="metodo_pago_enum"), default="efectivo")
    estado      = db.Column(db.Enum("abierta", "cerrada", "cancelada", name="estado_enum"), default="abierta")
    usuario_id  = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    creado_en   = db.Column(db.DateTime, default=datetime.utcnow)

    detalles    = db.relationship("DetalleVenta", backref="venta", lazy=True)

    def __repr__(self):
        return f"<Venta {self.folio}>"