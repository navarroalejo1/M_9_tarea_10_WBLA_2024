from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

def crear_layout(data):
    """Crea el diseño de la interfaz gráfica."""
    
    return dbc.Container([
        html.H1("Análisis Deportivo: Altura CMJ y Molestias", className="text-center"),

        # 🔹 Filtros en dos columnas
        dbc.Row([
            dbc.Col([
                html.Label("Filtrar por Equipo"),
                dcc.Dropdown(
                    id='team-dropdown',
                    options=[{'label': equipo, 'value': equipo} for equipo in data['Equipo'].unique()],
                    placeholder="Selecciona un equipo"
                ),
            ], width=6),

            dbc.Col([
                html.Label("Filtrar por Jugador"),
                dcc.Dropdown(id='player-dropdown', placeholder="Selecciona un jugador"),
            ], width=6),
        ], className="mb-4"),

        # 🔹 Contenedor 1: Tabla de datos filtrados
        dbc.Row([
            dbc.Col([
                html.H3("📊 Datos Filtrados"),
                dash_table.DataTable(
                    id='tabla-datos-filtrados',
                    columns=[
                        {"name": "Fecha", "id": "Fecha"},
                        {"name": "Jugador", "id": "Jugador"},
                        {"name": "Equipo", "id": "Equipo"},
                        {"name": "CMJ Intento", "id": "CMJ Intento"},
                        {"name": "Altura CMJ (cm)", "id": "Altura CMJ (cm)"}
                    ],
                    page_size=10,
                    style_table={'overflowX': 'auto'}
                ),
            ], width=12),
        ], className="mb-4"),

        # 🔹 Contenedor 2: Gráfico de barras
        dbc.Row([
            dbc.Col([
                html.H3("📉 Gráfico de Barras"),
                dcc.Graph(id='grafico-barras'),
            ], width=12),
        ], className="mb-4"),

        # 🔹 Contenedor 3: Gráfico de línea con filtro de "Momento"
        dbc.Row([
            dbc.Col([
                html.Label("Filtrar por Momento:"),
                dcc.RadioItems(
                    id="moment-filter",
                    options=[{"label": momento, "value": momento} for momento in sorted(data["Momento"].unique())],
                    value="Pre",
                    inline=True
                ),
            ], width=3),

            dbc.Col([
                html.H3("📈 Gráfico de Línea"),
                dcc.Graph(id='grafico-linea'),
            ], width=9),
        ], className="mb-4"),
    ], fluid=True)
