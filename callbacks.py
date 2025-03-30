from dash import Input, Output, State, dcc
from flask_login import login_user, logout_user, current_user

from auth import validate_login, users, login_layout
from pages import home
from pages.performance import layout as layout_performance
from pages.lesiones import layout as layout_lesiones

def register_callbacks(app):
    # Control de navegación
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname")
    )
    def display_page(pathname):
        if not current_user.is_authenticated and pathname != "/login":
            return login_layout()
        if pathname == "/logout":
            logout_user()
            return login_layout("Sesión cerrada.")
        elif pathname == "/performance":
            return layout_performance
        elif pathname == "/lesiones":
            return layout_lesiones
        return home.layout

    # Callback de login
    @app.callback(
        Output("login-output", "children"),
        Input("login-button", "n_clicks"),
        State("username", "value"),
        State("password", "value"),
        prevent_initial_call=True
    )
    def login_user_callback(n_clicks, username, password):
        if validate_login(username, password):
            login_user(users[username])
            return dcc.Location(href="/", id="redirect")
        return "Credenciales inválidas"
