from app.database import db


class DetalleVenta(db.Model):
    __tablename__ = "detalle_ventas"

    id = db.Column(db.Integer, primary_key=True)

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unit = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    venta_id = db.Column(
        db.Integer,
        db.ForeignKey("ventas.id"),
        nullable=False
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id"),
        nullable=False
    )

    producto = db.relationship(
        "Producto",
        back_populates="detalles"
    )

    def __repr__(self):
        return f"<DetalleVenta venta={self.venta_id} producto={self.producto_id}>"