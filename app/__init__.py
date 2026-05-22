import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # API olduğu için CORS ekliyoruz (Mobil cihazlar bağlanabilsin diye)
    CORS(app)
    
    app.config['SECRET_KEY'] = 'dev-secret-key'
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sofor_guvenlik.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # API Blueprint'ini kaydet
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
