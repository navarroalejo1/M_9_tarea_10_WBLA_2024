# auth.py

from flask import request
from flask_login import LoginManager, UserMixin
from dash import html, dcc

# Credenciales válidas
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin"

# Clase de usuario para Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = id
        self.authenticated = True

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return self.id

# Instancia de LoginManager
login_manager = LoginManager()
login_manager.login_view = "/login"

# Diccionario de usuarios válidos
users = {VALID_USERNAME: User(VALID_USERNAME)}

# Función que carga el usuario
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Validación de credenciales
def validate_login(username, password):
    return username == VALID_USERNAME and password == VALID_PASSWORD

# Layout de la pantalla de login con imagen y título personalizado
def login_layout(error=""):
    return html.Div([
        html.Div([
            html.H1("FIBA WBLA 2024", style={"color": "white", "marginBottom": "30px"}),
            html.Img(src="/assets/manu_rios.jpg", style={"height": "200px", "marginBottom": "30px"}),
            html.H2("Iniciar Sesión", style={"color": "white"}),
            dcc.Input(id="username", placeholder="Usuario", type="text"),
            html.Br(), html.Br(),
            dcc.Input(id="password", placeholder="Contraseña", type="password"),
            html.Br(), html.Br(),
            html.Button("Entrar", id="login-button"),
            html.Div(id="login-output", children=error, style={"color": "red", "marginTop": "10px"})
        ], style={
            "textAlign": "center",
            "backgroundColor": "#111",
            "padding": "40px",
            "borderRadius": "10px",
            "width": "400px",
            "margin": "auto",
            "color": "white"
        })
    ], style={"paddingTop": "80px"})
