from flask import app
from app import create_app
from config import config

environment = config['development']
app = create_app(environment)
if __name__ == "__main__":
    app.run(debug=True, port=4000)
    