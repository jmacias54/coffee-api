# app/utils.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
import json

def rol_requerido(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = json.loads(get_jwt_identity())
            if identity["rol"] not in roles:
                return jsonify({
                    "error": f"Acceso denegado. Se requiere rol: {', '.join(roles)}"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator