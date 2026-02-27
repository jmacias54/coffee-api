# app/__init__.py
from flask import Flask
from flask_restx import Api
from app.database import db
from app.config import Config

from flask_jwt_extended import JWTManager

from app.routes.categoria_routes import categoria_ns
from app.routes.producto_routes import producto_ns
from app.routes.usuario_routes import usuario_ns
from app.routes.venta_routes import venta_ns
from app.routes.auth_routes import auth_ns
from app.routes.reporte_routes import reporte_ns
from app.routes.corte_routes import corte_ns
from app.errors.handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["DEBUG"] = True
    db.init_app(app)


    # Inicializar JWT
    JWTManager(app)

      # Inicializar Swagger
    api = Api(
        app,
        version="1.0",
        title="Cafetería API",
        description="API REST para el punto de venta de la cafetería",
        doc="/",
        authorizations={
            "Bearer": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Agrega: Bearer {token}"
            }
        },
        security="Bearer"
    )

    api.add_namespace(categoria_ns)
    api.add_namespace(producto_ns)
    api.add_namespace(usuario_ns)
    api.add_namespace(venta_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(reporte_ns)
    api.add_namespace(corte_ns)

    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(categoria_ns, path="/categorias")
    api.add_namespace(producto_ns, path="/productos")
    api.add_namespace(usuario_ns, path="/usuarios")
    api.add_namespace(venta_ns, path="/ventas")
    api.add_namespace(reporte_ns, path="/reportes")
    api.add_namespace(corte_ns, path="/corte")


    register_error_handlers(app)

    return app