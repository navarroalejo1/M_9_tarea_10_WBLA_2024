from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # 🔹 Barra de navegación mejorada
    dbc.Navbar(
        dbc.Container([
            # 👉 Logo + Nombre
            dbc.NavbarBrand(
                html.Div([
                    html.Img(src="/assets/logo_fiba.jpg", height="70px", style={"marginRight": "10px"}),
                    html.Span("FIBA WBLA 2024", style={"fontWeight": "bold", "fontSize": "20px", "color": "black"})
                ], style={"display": "flex", "alignItems": "center"}),
                href="/"
            ),

            # 👉 Botón colapsable en dispositivos pequeños
            dbc.NavbarToggler(id="navbar-toggler"),

            # 👉 Menú de navegación
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Inicio", href="/", style={"color": "Blue"})),
                    dbc.NavItem(dbc.NavLink("Performance", href="/performance", style={"color": "Black"})),
                    dbc.NavItem(dbc.NavLink("Lesiones", href="/lesiones", style={"color": "Black"})),
                    dbc.NavItem(dbc.NavLink("Salir", href="/logout", style={"color": "Red"})),
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                navbar=True,
            ),
        ]),
        color="dark",
        dark=True,
        sticky="top"
    ),

    html.Div(id="page-content")
])
