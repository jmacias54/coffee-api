# app/schemas/producto_schema.py
from flask_restx import fields

def producto_model(api):
    return api.model("Producto", {
        "id":           fields.Integer(readonly=True),
        "nombre":       fields.String(required=True, description="Nombre del producto"),
        "descripcion":  fields.String(description="Descripción del producto"),
        "precio":       fields.Float(required=True, description="Precio del producto"),
        "stock":        fields.Integer(default=0),
        "activo":       fields.Boolean(default=True),
        "imagen_url":   fields.String(description="URL de la imagen"),
        "categoria_id": fields.Integer(required=True, description="ID de la categoría"),
        "creado_en":    fields.DateTime(readonly=True)
    })

def producto_input_model(api):
    return api.model("ProductoInput", {
        "nombre":       fields.String(required=True, description="Nombre del producto"),
        "descripcion":  fields.String(description="Descripción del producto"),
        "precio":       fields.Float(required=True, description="Precio del producto"),
        "stock":        fields.Integer(default=0),
        "activo":       fields.Boolean(default=True),
        "imagen_url":   fields.String(description="URL de la imagen"),
        "categoria_id": fields.Integer(required=True, description="ID de la categoría")
    })