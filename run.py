from app import create_app
import logging
from app import create_app

# configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = create_app()

if __name__ == "__main__":
       app.run(debug=True, use_reloader=False)

    