from api import create_app
from dotenv import load_dotenv

load_dotenv()
app = create_app()

# flask --app wsgi.py --debug run
if __name__ == "__main__":
    app.run()
