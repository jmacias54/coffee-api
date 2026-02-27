# app/schemas/venta_schema.py
from flask_restx import fields
from app.schemas.detalle_venta_schema import detalle_venta_input_model

def venta_model(api):
    return api.model("Venta", {
        "id":          fields.Integer(readonly=True),
        "folio":       fields.String(readonly=True),
        "total":       fields.Float(readonly=True),
        "pagado_con":  fields.Float(required=True),
        "cambio":      fields.Float(readonly=True),
        "metodo_pago": fields.String(default="efectivo"),
        "estado":      fields.String(readonly=True),
        "usuario_id":  fields.Integer(required=True),
        "creado_en":   fields.DateTime(readonly=True)
    })

def venta_input_model(api):
    return api.model("VentaInput", {
        "pagado_con":  fields.Float(required=True),
        "metodo_pago": fields.String(default="efectivo"),
        "usuario_id":  fields.Integer(required=True),
        "detalles":    fields.List(fields.Nested(detalle_venta_input_model(api)), required=True)
    })