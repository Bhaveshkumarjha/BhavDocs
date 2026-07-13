import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)

    # -----------------------------
    # Security / Session
    # -----------------------------
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-secret")

    # -----------------------------
    # Database Configuration
    # -----------------------------
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # Render PostgreSQL support
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://", "postgresql://", 1
            )

        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        # Local SQLite (for local development)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/dms.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # -----------------------------
    # Mail Configuration
    # -----------------------------
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

    # -----------------------------
    # Password Reset Salt
    # -----------------------------
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
        "SECURITY_PASSWORD_SALT",
        "fallback-salt"
    )

    # -----------------------------
    # Initialize Extensions
    # -----------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # -----------------------------
    # Register Blueprints
    # -----------------------------
    from . import routes
    app.register_blueprint(routes.bp)

    return app
