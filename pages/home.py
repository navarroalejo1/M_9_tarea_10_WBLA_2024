from dash import html
import dash_bootstrap_components as dbc
from data_loader import load_lesiones

# Cargar los equipos desde cmj_lesiones.csv
df_lesiones = load_lesiones()

# Validación: asegurar que la columna 'equipo' exista
if "equipo" not in df_lesiones.columns:
    raise KeyError("❌ ERROR: La columna 'equipo' no se encuentra en cmj_lesiones.csv.")

# Obtener lista única de equipos
equipos_unicos = sorted(df_lesiones["equipo"].dropna().unique())

# Dividir en dos columnas visuales (mitad/mitad)
mid_index = len(equipos_unicos) // 2
col1 = equipos_unicos[:mid_index]
col2 = equipos_unicos[mid_index:]

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src="/assets/carolina.jpg", style={"width": "60%"}), width=6, style={"textAlign": "center"}),
        dbc.Col(html.Img(src="/assets/logo_fiba.jpg", style={"width": "30%"}), width=6, style={"textAlign": "center"}),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(html.H2("Equipos Participantes", style={"color": "black", "textAlign": "center"}), width=12),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.Ul([html.Li(equipo, style={"fontSize": "18px", "color": "#222"}) for equipo in col1])
            ], style={"padding": "0 1rem"})
        ], width=6),

        dbc.Col([
            html.Div([
                html.Ul([html.Li(equipo, style={"fontSize": "18px", "color": "#222"}) for equipo in col2])
            ], style={"padding": "0 1rem"})
        ], width=6),
    ], className="mb-5")
], fluid=True, style={"backgroundColor": "white"})
