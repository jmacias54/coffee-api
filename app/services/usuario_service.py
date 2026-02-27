from app.repositories.usuario_repo import UsuarioRepo
from werkzeug.security import generate_password_hash


class UsuarioService:

    def __init__(self):
        self.repo = UsuarioRepo()

    def obtener_todos(self):
        return self.repo.obtener_todos()

    def obtener_por_id(self, id):
        usuario = self.repo.obtener_por_id(id)
        if not usuario:
            raise ValueError(f"Usuario con id {id} no encontrado")
        return usuario

    def crear(self, data):
        nombre = data.get("nombre")
        email = data.get("email")
        password = data.get("password")

        if not nombre:
            raise ValueError("El nombre es requerido")
        if not email:
            raise ValueError("El email es requerido")
        if not password:
            raise ValueError("El password es requerido")

        if self.repo.obtener_por_email(email):
            raise ValueError("Ya existe un usuario con ese email")

        usuario = {
            "nombre": nombre,
            "email": email,
            "password": generate_password_hash(password),
            "rol": data.get("rol", "cajero"),
            "activo": data.get("activo", True)
        }

        return self.repo.crear(usuario)

    def actualizar(self, id, data):
        usuario = self.obtener_por_id(id)

        if "email" in data:
            existente = self.repo.obtener_por_email(data["email"])
            if existente and existente.id != id:
                raise ValueError("Ya existe un usuario con ese email")

        if "password" in data:
            data["password"] = generate_password_hash(data["password"])

        return self.repo.actualizar(id, data)

    def eliminar(self, id):
        usuario = self.obtener_por_id(id)
        return self.repo.eliminar(id)