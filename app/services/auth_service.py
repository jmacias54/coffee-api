# app/services/auth_service.py
import json

from app.repositories.usuario_repo import UsuarioRepo
from flask_jwt_extended import create_access_token
import hashlib
from werkzeug.security import check_password_hash


repo = UsuarioRepo()

class AuthService:

    def login(self, email, password):
        if not email or not password:
            raise ValueError("Email y password son requeridos")

        # buscar usuario por email
        usuario = repo.obtener_por_email(email)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # verificar que esté activo
        if not usuario.activo:
            raise ValueError("Usuario inactivo, contacta al administrador")

        # encriptar password y comparar
        if not check_password_hash(usuario.password, password):
            raise ValueError("Credenciales inválidas")

        # generar token JWT con info del usuario
         # identity debe ser string en versiones nuevas de flask-jwt-extended
        identity = json.dumps({
            "id":     usuario.id,
            "nombre": usuario.nombre,
            "email":  usuario.email,
            "rol":    usuario.rol
        })

        token = create_access_token(identity=identity)



        return {
            "token":  token,
            "nombre": usuario.nombre,
            "email":  usuario.email,
            "rol":    usuario.rol
        }