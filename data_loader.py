import pandas as pd


def cargar_cmj_lesiones():
    df = pd.read_csv("data/cmj_lesiones.csv")
    df.columns = df.columns.str.strip().str.lower()  # normalizar nombres de columnas
    return df

# Función general para cargar CSV
def load_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        print(f"Error cargando {filepath}: {e}")
        return pd.DataFrame()

# Carga específica de archivos
def load_equipos():
    return load_csv("data/equipos.csv")

def load_boxscore():
    return load_csv("data/boxscore_limpio.csv")

def load_lesiones():
    return load_csv("data/cmj_lesiones.csv")

# cargar lesiones.py
cargar_cmj_lesiones = load_lesiones

# Cargar equipos como opciones para dropdown
def load_teams():
    df = load_equipos()
    if "team" not in df.columns:
        raise KeyError("Falta la columna 'team'")
    return [{"label": t, "value": t} for t in df["team"].dropna().unique()]

# Obtener lista de partidos únicos
def get_partidos():
    df = load_boxscore()
    return df[['fecha', 'match_id', 'team']].drop_duplicates()

# Obtener datos de un partido específico
def get_partidos_ID(match_id):
    df = load_boxscore()
    return df[df["match_id"] == match_id]

# Estadísticas por jugador
def get_stats_by_player():
    return load_boxscore()

# Estadísticas agregadas por partido
def get_stats_by_match():
    df = load_boxscore()
    if df is not None and not df.empty:
        df["Partido"] = df.groupby(["match_id", "fecha"])["team"].transform(lambda x: " vs ".join(sorted(x.unique())))
        return df.groupby(["fecha", "Partido"])[["pts", "ast", "reb", "oreb", "dreb", "per", "tap"]].sum().reset_index()
    return pd.DataFrame()
