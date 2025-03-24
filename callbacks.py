import pandas as pd
import plotly.express as px
from dash import Input, Output, dash_table

def registrar_callbacks(app, data):
    """
    Define y registra los callbacks de la aplicación Dash.
    """

    # 🔹 Callback para actualizar los jugadores según el equipo seleccionado
    @app.callback(
        Output("player-dropdown", "options"),
        [Input("team-dropdown", "value")]
    )
    def update_players(selected_team):
        jugadores = data[data["Equipo"] == selected_team]["Jugador"].unique()
        return [{"label": jugador, "value": jugador} for jugador in jugadores]

    # 🔹 Callback para actualizar la tabla
    @app.callback(
        Output("tabla-datos-filtrados", "data"),
        [Input("team-dropdown", "value"),
         Input("player-dropdown", "value")]
    )
    def update_table(selected_team, selected_player):
        filtered_data = data[
            (data["Equipo"] == selected_team) & 
            (data["Jugador"] == selected_player)
        ][["Fecha", "Jugador", "Equipo", "CMJ Intento", "Altura CMJ (cm)"]]

        return filtered_data.to_dict("records")

    # 🔹 Callback para actualizar el gráfico de barras
    @app.callback(
        Output("grafico-barras", "figure"),
        [Input("team-dropdown", "value"),
         Input("player-dropdown", "value")]
    )
    def update_bar_chart(selected_team, selected_player):
        filtered_data = data[
            (data["Equipo"] == selected_team) &
            (data["Jugador"] == selected_player)
        ]

        fig = px.bar(filtered_data, x="Fecha", y=["CMJ Intento", "Altura CMJ (cm)"],
                     title=f"CMJ Intento y Altura CMJ - {selected_player}",
                     barmode="group")

        return fig

    # 🔹 Callback para actualizar el gráfico de líneas con filtro de "Momento"
    @app.callback(
        Output("grafico-linea", "figure"),
        [Input("team-dropdown", "value"),
         Input("player-dropdown", "value"),
         Input("moment-filter", "value")]
    )
    def update_line_chart(selected_team, selected_player, moment):
        filtered_data = data[
            (data["Equipo"] == selected_team) &
            (data["Jugador"] == selected_player) &
            (data["Momento"] == moment)
        ]

        fig = px.line(filtered_data, x="Fecha", y=["CMJ Intento", "Altura CMJ (cm)"],
                      title=f"Evolución de CMJ en {moment} - {selected_player}",
                      markers=True)

        return fig
