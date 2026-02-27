from app.database import db
from app.models.producto import Producto
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError


class ProductoRepo:

    def obtener_todos(self):
        return Producto.query.filter_by(activo=True).all()

    def obtener_por_id(self, id):
        return db.session.get(Producto, id)

    def obtener_por_categoria(self, categoria_id):
        return Producto.query.filter_by(
            categoria_id=categoria_id,
            activo=True
        ).all()

    def obtener_por_nombre_y_categoria(self, nombre, categoria_id):
        return Producto.query.filter(
            func.lower(Producto.nombre) == nombre.lower(),
            Producto.categoria_id == categoria_id,
            Producto.activo == True
        ).first()

    def crear(self, producto):
        try:
            db.session.add(producto)
            db.session.commit()
            return producto
        except IntegrityError:
            db.session.rollback()
            raise

    def actualizar(self):
        db.session.commit()

    def eliminar(self, producto):
        producto.activo = False
        db.session.commit()