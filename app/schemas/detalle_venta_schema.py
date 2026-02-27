# app/schemas/detalle_venta_schema.py
from flask_restx import fields

def detalle_venta_model(api):
    return api.model("DetalleVenta", {
        "id":          fields.Integer(readonly=True),
        "cantidad":    fields.Integer(required=True),
        "precio_unit": fields.Float(required=True),
        "subtotal":    fields.Float(readonly=True),
        "venta_id":    fields.Integer(readonly=True),
        "producto_id": fields.Integer(required=True)
    })

def detalle_venta_input_model(api):
    return api.model("DetalleVentaInput", {
        "cantidad":    fields.Integer(required=True),
        "producto_id": fields.Integer(required=True)
    })