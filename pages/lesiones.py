from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data_loader import load_lesiones

df_lesiones = load_lesiones()

# 📌 Generar opciones del dropdown de equipos
equipos_options = [{'label': e, 'value': e} for e in sorted(df_lesiones["equipo"].dropna().unique())]

layout = dbc.Container([
    html.H3("⚕️ Análisis de Lesiones y Rendimiento", className="text-center mb-4"),

    # 🔹 Filtro de Equipo
    dbc.Row([
        dbc.Col([
            html.Label("Seleccionar Equipo:", className="fw-bold"),
            dcc.Dropdown(
                id="equipo-dropdown",
                options=equipos_options,
                placeholder="Seleccione un equipo",
                multi=False,
                className="mb-3"
            ),
        ], width=6),
    ], className="mb-4"),

    # 📌 Gráficos de lesiones
    dbc.Container([dcc.Graph(id="grafico-molestias")], className="mb-5"),
    dbc.Container([dcc.Graph(id="grafico-molestias-equipo")], className="mb-5"),
])

# 📌 Callbacks para actualizar gráficos según equipo seleccionado
@callback(Output("grafico-molestias", "figure"), Input("equipo-dropdown", "value"))
def update_molestias(equipo):
    df_filtered = df_lesiones if not equipo else df_lesiones[df_lesiones["equipo"] == equipo]
    fig = px.histogram(df_filtered, x="molestias", title=f"Distribución de Molestias - {equipo if equipo else 'Todos'}")
    return fig

@callback(Output("grafico-molestias-equipo", "figure"), Input("equipo-dropdown", "value"))
def update_molestias_equipo(equipo):
    df_filtered = df_lesiones if not equipo else df_lesiones[df_lesiones["equipo"] == equipo]
    fig = px.bar(df_filtered, x="equipo", y="molestias", title=f"Molestias por Equipo - {equipo if equipo else 'Todos'}", barmode="group")
    return fig
