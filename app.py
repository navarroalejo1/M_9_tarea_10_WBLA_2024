# app.py

from dash import Dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask_login import current_user

from layout import layout as layout_principal
from callbacks import register_callbacks
from auth import login_manager, login_layout

# Inicializar servidor Flask
flask_app = Flask(__name__)
flask_app.secret_key = "superclave123"  # Cambia esta clave en producción

# Configurar Flask-Login
login_manager.init_app(flask_app)

# Inicializar Dash
app = Dash(
    __name__,
    server=flask_app,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = "FIBA WBLA 2024"

# Layout condicional según autenticación
app.layout = lambda: login_layout() if not current_user.is_authenticated else layout_principal

# Registrar callbacks
register_callbacks(app)

# Correr app
if __name__ == "__main__":
    app.run(debug=True)
