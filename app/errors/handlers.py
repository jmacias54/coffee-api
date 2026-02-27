
import traceback

def register_error_handlers(app):

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return {"error": str(e)}, 400

    @app.errorhandler(Exception)
    def handle_general_error(e):
        return {"error": "Error interno del servidor"}, 500
    
    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return {"error": str(e)}, 400

    @app.errorhandler(Exception)
    def handle_general_error(e):
        print("🔥 ERROR DETECTADO:")
        traceback.print_exc() 
        return {"error": "Error interno del servidor"}, 500