from flask_restx import fields

def login_input_model(api):
    return api.model("LoginInput", {
        "email":    fields.String(required=True, description="Email del usuario"),
        "password": fields.String(required=True, description="Password del usuario")
    })

def login_response_model(api):
    return api.model("LoginResponse", {
        "token":  fields.String(description="Token JWT"),
        "nombre": fields.String(description="Nombre del usuario"),
        "email":  fields.String(description="Email del usuario"),
        "rol":    fields.String(description="Rol del usuario")
    })