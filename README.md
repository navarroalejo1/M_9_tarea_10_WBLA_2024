# 🏀 Análisis Deportivo: FIBA WBLA 2024  y CMJ y Molestias de competencia

Aplicación desarrollada con **Dash**, **Plotly** y **Bootstrap** para la visualización e interpretación de datos de rendimiento físico (altura CMJ) y molestias de los jugadores por equipo y momento del test.

---

## 📦 Estructura del Proyecto

```
├── app.py                    # Entrada principal de la app Dash
├── auth.py                  # Lógica de autenticación
├── callbacks.py             # Callbacks globales 
├── data_loader.py           # Carga de CSV desde data/
├── layout.py                # Navbar, sidebar y layout generales
├── assets/
│   └── styles.css           # Estilos personalizados 
├── data/
│   ├── cmj_lesiones.csv     # Datos físicos y molestias
│   └── boxscore_limpio.csv # Estadísticas de partido
├── pages/
│   ├── home.py              # Visualización por equipos
│   ├── lesiones.py          # Gráficos CMJ y molestias
│   └── performance.py       # Estadísticas individuales
├── requirements.txt         # Librerías necesarias
├── README.md                # Documentación del proyecto
```

---

## 🚀 Cómo ejecutar la app

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/navarroalejo1/M_9_tarea_10_LESIONES_2.git
cd M_9_tarea_10_LESIONES_2
```

### 2️⃣ Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv .venv
.venv\Scripts\activate  # En Windows
# source .venv/bin/activate  # En Linux/Mac
```

### 3️⃣ Instalar requerimientos

```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar la app

```bash
python app.py
```

## 🧠 Funcionalidades clave

- Filtros por equipo, jugador y momento
- Gráficos dinámicos con Plotly:
  - Altura CMJ por fecha e intento
  - Evolución temporal del rendimiento
  - Dispersión CMJ vs molestias
  - Conteo de molestias por zona anatómica
- Tablas interactivas de datos filtrados
- Exportación a PDF
- Tarjetas resumen por jugador (CMJ promedio, máximo, mínimo y molestias más frecuentes)

---

## 👨‍💻 Autor

Desarrollado por **[ALEJANDRO NAVARRO R ]** como herramienta para el análisis metodológico deportivo.  
📧 Contacto: [navarroalejo@hotmail.com]
