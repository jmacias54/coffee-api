# app/models/usuario.py
from app.database import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id         = db.Column(db.Integer, primary_key=True)
    nombre     = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), nullable=False, unique=True)
    password   = db.Column(db.String(255), nullable=False)
    rol        = db.Column(db.Enum("admin", "cajero", name="rol_enum"), default="cajero")
    activo     = db.Column(db.Boolean, default=True)
    creado_en  = db.Column(db.DateTime, default=datetime.utcnow)

    ventas     = db.relationship("Venta", backref="usuario", lazy=True)

    def __repr__(self):
        return f"<Usuario {self.email}>"