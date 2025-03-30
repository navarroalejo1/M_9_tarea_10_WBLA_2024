from dash import dcc, html, callback, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from dash.exceptions import PreventUpdate
from data_loader import get_partidos, get_partidos_ID, get_stats_by_player
import os

# ✅ Obtener datos iniciales de los partidos
partidos = get_partidos()
partidos_unicos = partidos.groupby(["fecha", "match_id"])["team"].apply(
    lambda x: " vs ".join(sorted(x.unique()))
).reset_index()

# ✅ Layout de la página de performance
layout = dbc.Container([
    html.H3("📊 Performance Equipo", className="text-center"),

    ## 🔹 PRIMER CONTENEDOR
    dbc.Container([
        html.H4("🗓️ Seleccionar Fecha y Partido", style={"color": "orange", "textAlign": "center"}),
        dbc.Row([
            dbc.Col(dcc.Dropdown(id="fecha-dropdown",
                                 options=[{"label": f, "value": f} for f in partidos_unicos["fecha"].unique()],
                                 placeholder="Selecciona una fecha"), width=6),
            dbc.Col(dcc.Dropdown(id="partido-dropdown",
                                 placeholder="Selecciona un partido"), width=6),
        ], className="mb-3"),
        dbc.Row(id="estadisticas-clave-container")
    ], className="mb-5"),

    ## 🔹 SEGUNDO CONTENEDOR
    html.H3("📊 Performance jugadores", className="text-center"),
    dbc.Container([
        html.H4("🗓️ Seleccionar Fecha y Partido", style={"color": "orange", "textAlign": "center"}),
        dbc.Row([
            dbc.Col(dcc.Dropdown(id="fecha-dropdown-player",
                                 options=[{"label": f, "value": f} for f in partidos_unicos["fecha"].unique()],
                                 placeholder="Selecciona una fecha"), width=4),
            dbc.Col(dcc.Dropdown(id="match-dropdown-player",
                                 placeholder="Selecciona un partido"), width=4),
            dbc.Col(dcc.Dropdown(id="equipo-dropdown",
                                 placeholder="Selecciona un equipo"), width=4)
        ], className="mb-3"),
        dash_table.DataTable(id="player-stats-table",
            columns=[{"name": col, "id": col} for col in [
                "jugadores", "min", "pts", "oreb", "dreb", "reb", "ast", "fp", "per",
                "rob", "tap", "+/-", "efc", "tcc", "tci", "2pc", "2pi", "3pc", "3pi", "tlc", "tli"]],
            style_header={"backgroundColor": "orange", "color": "black"},
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center"}
        ),
        html.Br(),
        dbc.Button("📄 Exportar tabla a PDF", id="export-pdf-button", color="primary", className="mb-3"),
        html.Div(id="pdf-download-link")
    ], className="mb-5"),

    ## 🔹 TERCER CONTENEDOR
    html.H3("📈 Estadísticas por Jugador", className="text-center"),
    dbc.Container([
        dcc.Graph(id="grafico-estadisticas-partido")
    ], className="mb-5")
], fluid=True)

# ✅ Callback: Lista de partidos por fecha
@callback(Output("partido-dropdown", "options"), Input("fecha-dropdown", "value"))
def update_partidos(fecha):
    df = get_partidos()
    if fecha:
        partidos_filtrados = df[df["fecha"] == fecha]
        partidos_unicos = partidos_filtrados.groupby("match_id")["team"].apply(
            lambda x: " vs ".join(sorted(x.unique()))
        ).reset_index()
        return [{"label": row["team"], "value": row["match_id"]} for _, row in partidos_unicos.iterrows()]
    return []

# ✅ Callback: Partidos por fecha para tabla
@callback(Output("match-dropdown-player", "options"), Input("fecha-dropdown-player", "value"))
def update_match_dropdown_player(fecha):
    opciones = partidos_unicos[partidos_unicos["fecha"] == fecha]
    return [{"label": row["team"], "value": row["match_id"]} for _, row in opciones.iterrows()]

# ✅ Callback: Equipos disponibles por partido
@callback(Output("equipo-dropdown", "options"), Input("match-dropdown-player", "value"))
def update_equipos_dropdown(match_id):
    df = get_stats_by_player()
    if match_id:
        equipos = df[df["match_id"] == match_id]["team"].unique()
        return [{"label": eq, "value": eq} for eq in equipos]
    return []

# ✅ Callback: Tabla de estadísticas por jugador
@callback(Output("player-stats-table", "data"),
          Input("match-dropdown-player", "value"),
          Input("equipo-dropdown", "value"))
def update_player_table(match_id, equipo):
    df = get_stats_by_player()
    if match_id and equipo:
        df_filtrado = df[(df["match_id"] == match_id) & (df["team"] == equipo)]
        return df_filtrado[[
            "jugadores", "min", "pts", "oreb", "dreb", "reb", "ast", "fp", "per",
            "rob", "tap", "+/-", "efc", "tcc", "tci", "2pc", "2pi", "3pc", "3pi", "tlc", "tli"
        ]].to_dict("records")
    return []

# ✅ Callback: Gráfico comparativo por jugador
@callback(Output("grafico-estadisticas-partido", "figure"), Input("partido-dropdown", "value"))
def update_estadisticas_partido(match_id):
    if not match_id:
        return go.Figure().update_layout(title="Selecciona un partido para ver las estadísticas")
    df = get_partidos_ID(match_id)
    if df.empty:
        return go.Figure().update_layout(title="No hay datos disponibles para este partido")

    equipos = " vs ".join(sorted(df["team"].unique()))
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["jugadores"], y=df["pts"], name="Puntos"))
    fig.add_trace(go.Bar(x=df["jugadores"], y=df["reb"], name="Rebotes"))
    fig.add_trace(go.Bar(x=df["jugadores"], y=df["ast"], name="Asistencias"))
    fig.update_layout(title=f"Estadísticas del Partido: {equipos}", barmode="group")
    return fig


@callback(Output("estadisticas-clave-container", "children"),
          Input("partido-dropdown", "value"))
def render_estadisticas_clave(match_id):
    if not match_id:
        return html.Div("Selecciona un partido para ver las estadísticas")

    df = get_partidos_ID(match_id)
    if df.empty:
        return html.Div("No hay datos disponibles para este partido")

    resumen = df.groupby("team")[["pts", "reb", "oreb", "dreb", "ast", "rob", "tap", "per"]].sum()
    if resumen.shape[0] != 2:
        return html.Div("Se necesitan dos equipos para mostrar la comparación")

    equipos = resumen.index.tolist()
    estadisticas = resumen.columns.tolist()
    max_valores = resumen.max().max()

    layout_barras = []
    for stat in estadisticas:
        val1 = resumen.loc[equipos[0], stat]
        val2 = resumen.loc[equipos[1], stat]
        porc1 = int((val1 / max_valores) * 100)
        porc2 = int((val2 / max_valores) * 100)

        barra = dbc.Row([
            dbc.Col(html.Div(style={
                "backgroundColor": "#007bff", "height": "20px", "width": f"{porc1}%",
                "textAlign": "right", "paddingRight": "5px", "color": "white"
            }, children=f"{val1}"), width=5),
            dbc.Col(html.Div(stat.upper(), style={"textAlign": "center", "fontWeight": "bold"}), width=2),
            dbc.Col(html.Div(style={
                "backgroundColor": "#dc3545", "height": "20px", "width": f"{porc2}%",
                "textAlign": "left", "paddingLeft": "5px", "color": "white"
            }, children=f"{val2}"), width=5)
        ], className="align-items-center mb-2")

        layout_barras.append(barra)

    return dbc.Container(layout_barras)


# ✅ Callback: Exportar a PDF
@callback(Output("pdf-download-link", "children"),
          Input("export-pdf-button", "n_clicks"),
          State("player-stats-table", "data"),
          prevent_initial_call=True)
def export_table_to_pdf(n_clicks, data):
    if not data:
        raise PreventUpdate

    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    columns = [
        "jugadores", "min", "pts", "oreb", "dreb", "reb", "ast", "fp", "per",
        "rob", "tap", "+/-", "efc", "tcc", "tci", "2pc", "2pi", "3pc", "3pi", "tlc", "tli"
    ]

    for col in columns:
        pdf.cell(20, 8, col.upper(), border=1)
    pdf.ln()

    for row in data:
        for col in columns:
            pdf.cell(20, 8, str(row.get(col, "")), border=1)
        pdf.ln()

    path = "assets/performance_table.pdf"
    os.makedirs("assets", exist_ok=True)
    pdf.output(path)

    return html.A("📄 Descargar PDF", href=path, target="_blank", className="btn btn-success")
