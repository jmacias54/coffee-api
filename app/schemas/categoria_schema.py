# app/schemas/categoria_schema.py
from flask_restx import fields

def categoria_model(api):
    return api.model("Categoria", {
        "id":          fields.Integer(readonly=True),
        "nombre":      fields.String(required=True, description="Nombre de la categoría"),
        "descripcion": fields.String(description="Descripción de la categoría"),
        "activo":      fields.Boolean(default=True),
        "creado_en":   fields.DateTime(readonly=True)
    })

def categoria_input_model(api):
    return api.model("CategoriaInput", {
        "nombre":      fields.String(required=True, description="Nombre de la categoría"),
        "descripcion": fields.String(description="Descripción de la categoría"),
        "activo":      fields.Boolean(default=True)
    })