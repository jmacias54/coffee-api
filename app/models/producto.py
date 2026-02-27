from app.database import db
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint


class Producto(db.Model):
    __tablename__ = "productos"

    __table_args__ = (
        db.Index("idx_producto_categoria", "categoria_id"),
        db.Index("idx_producto_activo", "activo"),
        db.UniqueConstraint(
            "nombre",
            "categoria_id",
            name="uq_producto_nombre_categoria"
        ),
        CheckConstraint("precio > 0", name="check_precio_positivo"),
    )

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True)
    imagen_url = db.Column(db.String(255))

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id"),
        nullable=False
    )

    # 👇 ESTA ES LA PARTE QUE TE FALTABA
    categoria = db.relationship(
        "Categoria",
        back_populates="productos"
    )

    creado_en = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    actualizado_en = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    detalles = db.relationship(
        "DetalleVenta",
        back_populates="producto",
        lazy="select",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Producto {self.nombre}>"