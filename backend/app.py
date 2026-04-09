from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import init_db
from routes.auth import auth_bp
from routes.products import products
from routes.cart import cart_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://localhost:8000"]}})

    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(products)
    app.register_blueprint(cart_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)