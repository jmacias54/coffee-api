# app/schemas/usuario_schema.py
from flask_restx import fields

def usuario_model(api):
    return api.model("Usuario", {
        "id":        fields.Integer(readonly=True),
        "nombre":    fields.String(required=True),
        "email":     fields.String(required=True),
        "rol":       fields.String(default="cajero"),
        "activo":    fields.Boolean(default=True),
        "creado_en": fields.DateTime(readonly=True)
    })

def usuario_input_model(api):
    return api.model("UsuarioInput", {
        "nombre":   fields.String(required=True),
        "email":    fields.String(required=True),
        "password": fields.String(required=True),
        "rol":      fields.String(default="cajero"),
        "activo":   fields.Boolean(default=True)
    })