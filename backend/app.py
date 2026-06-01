from flask import Flask
from flask_cors import CORS
from config import Config
from models import init_db


from routes.auth import auth_bp
from routes.products import products
from routes.cart import cart_bp
from routes.animatronics import animatronics_bp
from routes.characters import characters_bp
from routes.cast import cast_bp
from routes.search import search_bp
from routes.homeimage import home_bp 
from routes.orders import orders_bp
from models import init_orders_db

from routes.admin import admin_bp

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(Config)
    
    CORS(app, resources={
        r"/api/*": {"origins": ["https://kysurfer.github.io", "http://localhost:5173", "http://localhost:8000", "*"]},
        r"/static/*": {"origins": "*"}
    })
    
    init_db()
    init_orders_db()
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(products)
    app.register_blueprint(cart_bp)
    app.register_blueprint(animatronics_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(cast_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp) 
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)