# ✅ LESIONES.PY con layout y callbacks completos y comentados

from dash import dcc, html, dash_table, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import base64
import os
from dash.exceptions import PreventUpdate
from data_loader import cargar_cmj_lesiones

# 🔹 Cargar datos y normalizar nombres de columnas
# La función cargar_cmj_lesiones() lee y devuelve un DataFrame con los datos de CMJ y molestias de jugadores, incluyendo columnas como fecha, jugador, equipo, altura del salto, molestias y momento del test.
data = cargar_cmj_lesiones()
data.columns = data.columns.str.lower()
data["jugador"] = data["jugador"].str.strip()

# 🔷 LAYOUT completo
layout = html.Div([
    html.H1("Análisis Deportivo: Altura CMJ y Molestias", className="text-center mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Filtrar por Equipo"),
            dcc.Dropdown(
                id='team-dropdown',
                options=[{'label': eq, 'value': eq} for eq in sorted(data['equipo'].dropna().unique())],
                placeholder="Selecciona un equipo"
            )
        ], xs=12, md=4),

        dbc.Col([
            html.Label("Filtrar por Jugador"),
            dcc.Dropdown(id='player-dropdown', placeholder="Selecciona un jugador")
        ], xs=12, md=4),
    ], className="mb-4"),

    html.Hr(),
    html.H4("📄 Datos Filtrados", className="mb-3"),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='tabla-datos-filtrados',
                columns=[{"name": col, "id": col} for col in [
                    "fecha", "jugador", "equipo", "cmj intento", "altura cmj (cm)", "molestias", "momento"]],
                page_size=10,
                style_table={'overflowX': 'auto'}
            ),
        ])
    ], className="mb-4"),

    html.Hr(),
    html.H4("📊 Análisis Gráfico", className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.Label("Filtrar por Momento (Barras):"),
            dcc.RadioItems(id="moment-filter-barras", options=[
    {"label": "Todos", "value": "todos"},
    {"label": "Pre", "value": "Pre"},
    {"label": "Post", "value": "Post"}
], value="todos", inline=True)
        ], xs=12, md=6),

        dbc.Col([
            html.Label("Filtrar por Momento (Línea):"),
            dcc.RadioItems(id="moment-filter-linea", options=[
    {"label": "Todos", "value": "todos"},
    {"label": "Pre", "value": "Pre"},
    {"label": "Post", "value": "Post"}
], value="todos", inline=True)
        ], xs=12, md=6)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='grafico-barras', style={"height": "400px"})
        ], xs=12, md=6),

        dbc.Col([
            dcc.Graph(id='grafico-linea', style={"height": "400px"})
        ], xs=12, md=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Filtrar por Momento (Dispersión):"),
            dcc.RadioItems(id="moment-filter-dispersion", options=[
    {"label": "Todos", "value": "todos"},
    {"label": "Pre", "value": "Pre"},
    {"label": "Post", "value": "Post"},
], value="todos", inline=True)
        ], xs=12, md=6),

        dbc.Col([
            html.Label("Filtrar por Momento (Molestias):"),
            dcc.RadioItems(id="moment-filter-molestias", options=[
    {"label": "Todos", "value": "todos"},
    {"label": "Pre", "value": "Pre"},
    {"label": "Post", "value": "Post"},
], value="todos", inline=True)
        ], xs=12, md=6)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='grafico-dispersion-altura', style={"height": "400px"})
        ], xs=12, md=6),

        dbc.Col([
            dcc.Graph(id='grafico-barras-molestias', style={"height": "400px"})
        ], xs=12, md=6)
    ], className="mb-5"),

    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Promedio CMJ"), html.H3(id="cmj-promedio")])), className="bg-primary text-white"),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("CMJ Máximo"), html.H3(id="cmj-max")])), className="bg-info text-white"),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("CMJ Mínimo"), html.H3(id="cmj-min")])), className="bg-warning text-white"),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Zona con más molestias"), html.H3(id="zona-mas-afectada")])), className="bg-danger text-white")
    ], className="mb-4")
])

# 🔁 Callback: Actualiza las opciones del dropdown de jugadores según el equipo seleccionado
@callback(
    Output("player-dropdown", "options"),
    Input("team-dropdown", "value")
)
def update_players(selected_team):
    if selected_team:
        jugadores = data[data["equipo"] == selected_team]["jugador"].dropna().unique()
        return [{"label": j, "value": j} for j in sorted(jugadores)]
    return []

# 🔁 Callback: Actualiza la tabla con los datos filtrados
@callback(
    Output("tabla-datos-filtrados", "data"),
    Input("team-dropdown", "value"),
    Input("player-dropdown", "value")
)
def update_table(equipo, jugador):
    if not equipo or not jugador:
        raise PreventUpdate
    df = data[(data["equipo"] == equipo) & (data["jugador"] == jugador)]
    df = df.dropna(subset=["fecha"])
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m-%d")
    return df.to_dict("records")

# 🔁 Callback: Gráfico de barras - Altura CMJ
@callback(
    Output("grafico-barras", "figure"),
    Input("team-dropdown", "value"),
    Input("player-dropdown", "value"),
    Input("moment-filter-barras", "value")
)
def update_bar_chart(team, player, moment):
    df = data[(data["equipo"] == team) & (data["jugador"] == player)]
    if moment == "Pre":
        df = df[df["momento"] == "Pre"]
    elif moment == "Post":
        df = df[df["momento"] == "Post"]
    elif moment == "vacio":
        df = df[df["momento"].isna()]
    df = df.dropna(subset=["fecha", "altura cmj (cm)"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")
    df["fecha_str"] = df["fecha"].dt.strftime("%Y-%m-%d")
    fig = px.bar(df, x="fecha_str", y="altura cmj (cm)", color="cmj intento", barmode="group", title=f"Altura CMJ - {player}")
    fig.update_traces(text=df["altura cmj (cm)"], textposition="outside")
    return fig

# 🔁 Callback: Gráfico de línea - Evolución CMJ
@callback(
    Output("grafico-linea", "figure"),
    Input("team-dropdown", "value"),
    Input("player-dropdown", "value"),
    Input("moment-filter-linea", "value")
)
def update_line_chart(team, player, moment):
    df = data[(data["equipo"] == team) & (data["jugador"] == player)]
    if moment == "Pre":
        df = df[df["momento"] == "Pre"]
    elif moment == "Post":
        df = df[df["momento"] == "Post"]
    elif moment == "vacio":
        df = df[df["momento"].isna()]
    df = df.dropna(subset=["fecha", "altura cmj (cm)", "cmj intento"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")
    df["fecha_str"] = df["fecha"].dt.strftime("%Y-%m-%d")
    fig = px.line(
        df,
        x="fecha_str",
        y="altura cmj (cm)",
        color="cmj intento",
        markers=True,
        title=f"Evolución CMJ - {player}"
    )
    return fig

# 🔁 Callback: Gráfico de molestias
@callback(
    Output("grafico-barras-molestias", "figure"),
    Input("team-dropdown", "value"),
    Input("player-dropdown", "value"),
    Input("moment-filter-molestias", "value")
)
def update_molestias(team, player, moment):
    df = data[(data["equipo"] == team) & (data["jugador"] == player)]
    if moment == "Pre":
        df = df[df["momento"] == "Pre"]
    elif moment == "Post":
        df = df[df["momento"] == "Post"]
    elif moment == "vacio":
        df = df[df["momento"].isna()]
    df = df.dropna(subset=["fecha", "molestias"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")
    df["fecha_str"] = df["fecha"].dt.strftime("%Y-%m-%d")
    conteo = df.groupby(["fecha_str", "molestias"]).size().reset_index(name="conteo")
    fig = px.bar(conteo, x="fecha_str", y="conteo", color="molestias", barmode="stack", title=f"Molestias - {player}")
    return fig

# 🔁 Callback: Dispersión altura vs molestias
@callback(
    Output("grafico-dispersion-altura", "figure"),
    Input("team-dropdown", "value"),
    Input("player-dropdown", "value"),
    Input("moment-filter-dispersion", "value")
)
def update_dispersion(team, player, moment):
    df = data[(data["equipo"] == team) & (data["jugador"] == player)]
    if moment == "Pre":
        df = df[df["momento"] == "Pre"]
    elif moment == "Post":
        df = df[df["momento"] == "Post"]
    elif moment == "vacio":
        df = df[df["momento"].isna()]
    df = df.dropna(subset=["altura cmj (cm)", "molestias", "fecha"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")
    fig = px.scatter(df, x="altura cmj (cm)", y="molestias", color=df["fecha"].dt.strftime("%Y-%m-%d"), title=f"Dispersión CMJ vs Molestias - {player}")
    return fig


# 🔁 Callback: Tarjetas de resumen de CMJ
@callback(
    Output("cmj-promedio", "children"),
    Output("cmj-max", "children"),
    Output("cmj-min", "children"),
    Output("zona-mas-afectada", "children"),
    Input("team-dropdown", "value"),
    Input("player-dropdown", "value")
)
def update_summary_cards(equipo, jugador):
    if not equipo or not jugador:
        raise PreventUpdate
    df = data[(data["equipo"] == equipo) & (data["jugador"] == jugador)]
    df = df.dropna(subset=["altura cmj (cm)"])
    if df.empty:
        return "-", "-", "-", "-"
    promedio = df["altura cmj (cm)"].mean()
    maximo = df["altura cmj (cm)"].max()
    minimo = df["altura cmj (cm)"].min()
    zona = df["molestias"].mode().iloc[0] if not df["molestias"].mode().empty else "-"
    return (
        f"{promedio:.2f} cm",
        f"{maximo:.2f} cm",
        f"{minimo:.2f} cm",
        zona
    )
