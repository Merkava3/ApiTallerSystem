from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS  # Asegúrate de haber importado CORS correctamente
from .models import db
from .Views import api_v1

app = Flask(__name__)
Migrate = Migrate(app, db)

def create_app(environment):
    app.config.from_object(environment)
    

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5000", "http://127.0.0.1:5000"]}})
    app.register_blueprint(api_v1)
    
    with app.app_context():
        db.init_app(app)
        db.create_all()
        #print(app.url_map) 
    @app.after_request
    def after_request(response):
        # Añadir encabezados CORS a la respuesta
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    return app
