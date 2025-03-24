import pandas as pd

def cargar_datos(ruta_csv):
    """Carga los datos del archivo CSV."""
    datos = pd.read_csv(ruta_csv)
    datos['Fecha'] = pd.to_datetime(datos['Fecha'])  # Convertir la columna de fecha
    return datos
