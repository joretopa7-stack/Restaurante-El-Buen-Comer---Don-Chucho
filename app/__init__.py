from flask import Flask
from config import Config
from app.extensions import db, login_manager
from app.models import Usuario

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Cargar usuario para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar blueprints
    from app.blueprints.cliente import cliente_bp
    from app.blueprints.mesero import mesero_bp
    from app.blueprints.cocina import cocina_bp
    from app.blueprints.auth import auth_bp   # lo crearemos opcionalmente

    app.register_blueprint(cliente_bp, url_prefix='/')
    app.register_blueprint(mesero_bp, url_prefix='/mesero')
    app.register_blueprint(cocina_bp, url_prefix='/cocina')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
        # Cargar datos iniciales (categorías, platos, usuarios, mesas)
        from app.models import init_data
        init_data()

    return app