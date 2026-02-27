# app/routes/auth_routes.py
from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.services.auth_service import AuthService
from app.schemas.auth_schema import login_input_model

auth_ns = Namespace("auth", description="Autenticación")
service = AuthService()

@auth_ns.route("/login")
class Login(Resource):

    @auth_ns.expect(login_input_model(auth_ns))
    @auth_ns.doc(description="Iniciar sesión y obtener token JWT")
    def post(self):
        data   = request.get_json()
        result = service.login(data["email"], data["password"])
        return result, 200

@auth_ns.route("/refresh")
class Refresh(Resource):

    @jwt_required()
    @auth_ns.doc(description="Renovar token JWT sin hacer login de nuevo")
    def post(self):
        identity  = get_jwt_identity()
        new_token = create_access_token(identity=identity)
        return {"token": new_token}, 200

@auth_ns.route("/me")
class Me(Resource):

    @jwt_required()
    @auth_ns.doc(description="Obtener info del usuario autenticado")
    def get(self):
        import json
        identity = json.loads(get_jwt_identity())
        return identity, 200