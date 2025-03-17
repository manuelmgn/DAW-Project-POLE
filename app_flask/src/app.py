"""Aplicación principal de Flask"""

from flask import Flask

from config.config import Config
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.userlog import log_bp
from routes.users import user_bp
from routes.others import others_bp
from routes.routes import bp as main_bp

app = Flask(__name__)
app.config.from_object(Config)


# Rexistra Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(log_bp)
app.register_blueprint(others_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    application = app
