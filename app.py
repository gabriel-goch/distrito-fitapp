import os
import logging
import secrets
import datetime
import threading

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)

# Configuración de seguridad para la clave secreta
app.secret_key = os.environ.get("SESSION_SECRET") or secrets.token_hex(32)

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///fitness_studio.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 20,
    "max_overflow": 10,
    "pool_timeout": 30,
}

# initialize the app with the extension
db.init_app(app)

# Setup CSRF protection
csrf = CSRFProtect(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return db.session.get(User, int(user_id))

# Inicializar optimizaciones de PostgreSQL en segundo plano
def initialize_db_optimizations():
    import time
    time.sleep(30)  # Esperar 30 segundos antes de optimizar
    if 'postgresql' in app.config["SQLALCHEMY_DATABASE_URI"]:
        try:
            from utils.postgresql import create_indexes
            with app.app_context():
                create_indexes()
                app.logger.info("Optimizaciones de PostgreSQL aplicadas con éxito")
        except Exception as e:
            app.logger.error(f"Error al aplicar optimizaciones de PostgreSQL: {e}")

# Solo iniciar optimizaciones en ambiente de producción
is_production = os.environ.get("FLASK_ENV") != "development"
if is_production and 'postgresql' in app.config["SQLALCHEMY_DATABASE_URI"]:
    optimization_thread = threading.Thread(target=initialize_db_optimizations, daemon=True)
    optimization_thread.start()
