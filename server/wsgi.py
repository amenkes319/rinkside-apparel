from api import create_app
app = create_app()

# flask --app wsgi.py --debug run
if __name__ == "__main__":
    app.run()
