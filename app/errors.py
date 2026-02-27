# app/errors.py
from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from jwt.exceptions import ExpiredSignatureError, DecodeError

def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Petición inválida", "detalle": str(e)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "No autorizado"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "No tienes permisos para realizar esta acción"}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Error interno del servidor"}), 500

    @app.errorhandler(NoAuthorizationError)
    def no_auth(e):
        return jsonify({"error": "Token no proporcionado"}), 401

    @app.errorhandler(InvalidHeaderError)
    def invalid_header(e):
        return jsonify({"error": "Token inválido en el header"}), 401

    @app.errorhandler(ExpiredSignatureError)
    def token_expired(e):
        return jsonify({"error": "Token expirado, inicia sesión de nuevo"}), 401

    @app.errorhandler(DecodeError)
    def token_invalid(e):
        return jsonify({"error": "Token inválido"}), 401