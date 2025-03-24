from dash import Dash, html, dcc, Input, Output
import pandas as pd
from callbacks import registrar_callbacks

# Cargar los datos reales desde tu archivo CSV
data = pd.read_csv("data/cmj_lesiones.csv")  # Asegúrate de que el archivo esté en la misma carpeta

# Inicialización de la aplicación Dash
app = Dash(__name__)
server = app.server  # Para despliegue en servidores web como Heroku

# Layout de la aplicación utilizando contenedores
app.layout = html.Div([
    html.H1("Dashboard de Lesiones y Rendimiento Deportivo", style={'textAlign': 'center'}),

    # Contenedor de filtros
    html.Div([
        html.Label("Selecciona un equipo:"),
        dcc.Dropdown(
            id="team-dropdown",
            options=[{"label": team, "value": team} for team in sorted(data["Equipo"].unique())],
            value=sorted(data["Equipo"].unique())[0]
        ),
        html.Label("Selecciona un jugador:"),
        dcc.Dropdown(id="player-dropdown"),
    ], style={'padding': '10px', 'border': '1px solid #ccc'}),

    # Contenedor de tabla
    html.Div([
        html.H3("Datos Filtrados"),
        dcc.Graph(id="table-display", style={"height": "300px"})
    ], style={'padding': '20px', 'border': '1px solid #ccc'}),

    # Contenedor de gráfico
    html.Div([
        html.H3("Gráfico de Altura CMJ vs Fecha"),
        html.Label("Filtrar por Momento:"),
        dcc.RadioItems(
            id="moment-filter",
            options=[{"label": momento, "value": momento} for momento in sorted(data["Momento"].unique())],
            value="Pre",  # Valor por defecto
            inline=True
        ),
        dcc.Graph(id="bar-chart")
    ], style={'padding': '20px', 'border': '1px solid #ccc'}),
])

# Registrar callbacks desde el archivo `callbacks.py`
registrar_callbacks(app, data)

if __name__ == "__main__":
    app.run(debug=True)
