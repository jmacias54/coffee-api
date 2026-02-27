from app.database import db
from app.models.usuario import Usuario
from sqlalchemy.exc import IntegrityError


class UsuarioRepo:

    def obtener_todos(self):
        return Usuario.query.filter_by(activo=True).all()

    def obtener_por_id(self, id):
        return db.session.get(Usuario, id)

    def obtener_por_email(self, email):
        return Usuario.query.filter_by(email=email).first()

    def crear(self, data):
        usuario = Usuario(
            nombre=data["nombre"],
            email=data["email"],
            password=data["password"],
            rol=data.get("rol", "cajero"),
            activo=data.get("activo", True)
        )
        try:
            db.session.add(usuario)
            db.session.commit()
            return usuario
        except IntegrityError:
            db.session.rollback()
            raise

    def actualizar(self, id, data):
        usuario = self.obtener_por_id(id)
        if not usuario:
            return None

        usuario.nombre = data.get("nombre", usuario.nombre)
        usuario.email = data.get("email", usuario.email)
        usuario.rol = data.get("rol", usuario.rol)
        usuario.activo = data.get("activo", usuario.activo)

        if "password" in data:
            usuario.password = data["password"]

        db.session.commit()
        return usuario

    def eliminar(self, id):
        usuario = self.obtener_por_id(id)
        if not usuario:
            return None

        usuario.activo = False
        db.session.commit()
        return usuario