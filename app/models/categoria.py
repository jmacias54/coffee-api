from app.database import db
from datetime import datetime, timezone


class Categoria(db.Model):
    __tablename__ = "categorias"

    __table_args__ = (
        db.Index("idx_categoria_activo", "activo"),
    )

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True)

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

    # 👇 relación bidireccional correcta
    productos = db.relationship(
        "Producto",
        back_populates="categoria",
        lazy="select"
    )

    def __repr__(self):
        return f"<Categoria {self.nombre}>"