from sqlalchemy import func

from app.database import db
from app.models.categoria import Categoria
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

class CategoriaRepo:

    def obtener_todos(self):
        return Categoria.query.filter_by(activo=True).all()

    def obtener_por_id(self, id):
        return db.session.get(Categoria, id)

    def obtener_por_nombre(self, nombre):
        return Categoria.query.filter(
            func.lower(Categoria.nombre) == nombre.lower()
        ).first()

    def crear(self, data):
        categoria = Categoria(
            nombre=data["nombre"],
            descripcion=data.get("descripcion"),
            activo=data.get("activo", True)
        )
        try:
            db.session.add(categoria)
            db.session.commit()
            return categoria
        except IntegrityError:
            db.session.rollback()
            raise

    def actualizar(self, id, data):
        categoria = self.obtener_por_id(id)
        if not categoria:
            return None

        categoria.nombre = data.get("nombre", categoria.nombre)
        categoria.descripcion = data.get("descripcion", categoria.descripcion)
        categoria.activo = data.get("activo", categoria.activo)

        db.session.commit()
        return categoria

    def eliminar(self, id):
        categoria = self.obtener_por_id(id)
        if not categoria:
            return None

        categoria.activo = False
        db.session.commit()
        return categoria