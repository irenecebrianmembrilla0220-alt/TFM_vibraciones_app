from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd


# =========================
# CONFIGURACIÓN VISUAL
# =========================

st.set_page_config(
    page_title="Evaluación de vibraciones",
    page_icon="🛠️",
    layout="wide"
)
st.caption("VERSIÓN WEB ACTUALIZADA - prueba 14 junio")
st.markdown("""
<style>
    /* =========================
       TEMA CLARO / FONDO BLANCO
       ========================= */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main {
        background-color: #f5f7fb !important;
        color: #111827 !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .block-container {
        padding-top: 2.2rem !important;
        padding-bottom: 1.0rem !important;
        padding-left: 1.3rem !important;
        padding-right: 1.3rem !important;
        max-width: 100% !important;
    }

    .main-title {
        background-color: #0b73b7;
        color: white !important;
        padding: 18px 18px;
        text-align: center;
        border-radius: 7px;
        font-size: 25px;
        font-weight: bold;
        letter-spacing: 5px;
        margin-top: 10px;
        margin-bottom: 22px;
        width: 100%;
        box-sizing: border-box;
        line-height: 1.25;
        min-height: 72px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: visible;
        white-space: normal;
        box-shadow: 0 2px 5px rgba(0,0,0,0.10);
    }

    /* Contenedores con borde en claro */
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[class*="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #d7dde8 !important;
        border-radius: 10px !important;
        padding: 0.70rem !important;
        box-shadow: 0 1px 4px rgba(15,23,42,0.05);
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.50rem !important;
    }

    h1, h2, h3, h4, h5, h6,
    p, li, label, .stMarkdown, span, div {
        color: #111827;
    }

    h1 {
        font-size: 1.55rem !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 1.30rem !important;
        margin-bottom: 0.45rem !important;
    }

    h3 {
        font-size: 1.18rem !important;
        margin-bottom: 0.40rem !important;
    }

    h4 {
        font-size: 1.02rem !important;
        margin-bottom: 0.30rem !important;
    }

    p, li, label, .stMarkdown {
        font-size: 0.90rem !important;
    }

    /* Inputs claros y compactos */
    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInput"] input,
    input,
    textarea {
        background-color: #ffffff !important;
        color: #111827 !important;
        border-color: #cfd6e4 !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 2.25rem !important;
    }

    div[data-testid="stNumberInput"] input {
        min-height: 2.25rem !important;
        font-size: 0.90rem !important;
    }

    div[data-testid="stNumberInput"] button {
        min-height: 2.25rem !important;
        height: 2.25rem !important;
        background-color: #eef3f8 !important;
        color: #111827 !important;
        border-color: #cfd6e4 !important;
    }

    .stSelectbox label,
    .stNumberInput label {
        font-size: 0.88rem !important;
        margin-bottom: 0.10rem !important;
        color: #111827 !important;
    }

    div[data-testid="stNumberInput"],
    div[data-testid="stSelectbox"] {
        margin-bottom: 0.10rem !important;
    }

    /* DROPDOWNS / DESPLEGABLES */
    div[data-baseweb="popover"], 
    div[data-baseweb="menu"], 
    ul[role="listbox"] {
        background-color: #ffffff !important;
        border: 1px solid #cfd6e4 !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1) !important;
    }

    div[data-baseweb="popover"] *, 
    div[data-baseweb="menu"] *, 
    ul[role="listbox"] * {
        color: #111827 !important;
    }

    li[role="option"], 
    div[data-baseweb="menu"] li,
    div[role="option"] {
        background-color: #ffffff !important;
        color: #111827 !important;
        padding: 6px 12px !important;
    }

    li[role="option"]:hover, 
    div[data-baseweb="menu"] li:hover,
    div[role="option"]:hover,
    li[data-highlighted="true"] {
        background-color: #e8eef7 !important;
        color: #0b73b7 !important;
        cursor: pointer;
    }

    /* Botones */
    div.stButton > button,
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #0b73b7 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 7px !important;
        height: 2.45em;
        width: 100%;
        border: none !important;
        padding: 0.25rem 0.85rem;
        font-size: 0.92rem;
    }

    div.stButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #095f96 !important;
        color: white !important;
    }

    /* Botones de formularios: mantener azul y texto blanco */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #0b73b7 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 7px !important;
        height: 2.45em;
        min-width: 210px;
        border: none !important;
        padding: 0.25rem 0.85rem;
        font-size: 0.92rem;
    }

    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #095f96 !important;
        color: white !important;
    }

    .custom-metric {
        margin-top: 2px;
        margin-bottom: 3px;
        padding-top: 1px;
    }

    .custom-metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        line-height: 1.1;
        margin-bottom: 0.12rem;
    }

    .custom-metric-value {
        font-size: 1.45rem;
        font-weight: 500;
        line-height: 1.08;
    }

    .metric-normal {
        color: #111827;
    }

    .metric-action,
    .metric-action .custom-metric-label,
    .metric-action .custom-metric-value {
        color: #f39c12 !important;
    }

    .metric-limit,
    .metric-limit .custom-metric-label,
    .metric-limit .custom-metric-value {
        color: #e74c3c !important;
    }

    /* Separadores entre secciones más oscuros y visibles */
    hr {
        margin-top: 0.60rem !important;
        margin-bottom: 0.60rem !important;
        border: none !important;
        border-top: 1.8px solid #4b5563 !important;
        opacity: 1 !important;
    }

    [data-testid="stDivider"] {
        border-color: #4b5563 !important;
        opacity: 1 !important;
    }

    .compact-text {
        font-size: 0.86rem !important;
        line-height: 1.18 !important;
        margin-bottom: 0.20rem !important;
        color: #374151 !important;
    }

    /* Pantalla de acceso */
    .access-heading {
        font-size: 1.55rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #111827 !important;
    }

    .access-title {
        font-size: 1.45rem;
        font-weight: 800;
        margin-bottom: 0.85rem;
        color: #111827 !important;
    }

    .access-text {
        font-size: 1.08rem;
        line-height: 1.70;
        margin-bottom: 0.8rem;
        color: #111827 !important;
    }

    .access-card-note {
        min-height: 10.6rem;
    }

    /* Recuadros visibles en tema claro */
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[class*="stVerticalBlockBorderWrapper"] {
        border: 2.5px solid #000000 !important;
        background-color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.12) !important;
        padding: 1.05rem !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div,
    div[class*="stVerticalBlockBorderWrapper"] > div {
        border-radius: 12px !important;
    }

    /* Tarjetas específicas de acceso */
    .access-card-content {
        border: none !important;
        background: transparent !important;
        padding: 0.10rem 0.15rem 0.25rem 0.15rem;
    }

    .access-columns-space {
        margin-top: 0.6rem;
    }

    /* Avisos propios */
    .alert-warning-custom {
        background-color: #ffe08a !important;
        border: 1.5px solid #f59e0b !important;
        color: #111827 !important;
        padding: 0.85rem 1rem !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.4rem !important;
    }

    .alert-success-custom {
        background-color: #d1fae5 !important;
        border: 1.5px solid #10b981 !important;
        color: #064e3b !important;
        padding: 0.85rem 1rem !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.4rem !important;
    }

    .alert-error-custom {
        background-color: #ff3b3b !important;
        border: 2px solid #cc0000 !important;
        color: #ffffff !important;
        padding: 0.85rem 1rem !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.4rem !important;
    }

    /* Tablas claras personalizadas */
    .tabla-scroll {
        width: 100%;
        overflow-x: auto;
        overflow-y: auto;
        border: 1.4px solid #111827;
        border-radius: 8px;
        background: #ffffff;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    table.tabla-clara {
        width: 100%;
        border-collapse: collapse;
        background-color: #ffffff !important;
        color: #111827 !important;
        font-size: 0.90rem;
    }

    table.tabla-clara thead th {
        background-color: #e8eef7 !important;
        color: #111827 !important;
        font-weight: 700;
        border: 1px solid #111827;
        padding: 0.55rem 0.65rem;
        text-align: left;
        white-space: nowrap;
    }

    table.tabla-clara tbody td {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #111827;
        padding: 0.50rem 0.65rem;
    }

    table.tabla-clara tbody tr:nth-child(even) td {
        background-color: #f6f8fc !important;
    }

    a.anchor-link, .anchor-link {
        display: none !important;
    }

    /* Refuerzo de columnas de la pantalla de acceso */
    div[data-testid="column"] div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stColumn"] div[class*="stVerticalBlockBorderWrapper"],
    div[class*="stColumn"] div[class*="stVerticalBlockBorderWrapper"] {
        border: 2.5px solid #000000 !important;
        background-color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.15) !important;
        padding: 1.15rem 1.25rem !important;
        min-height: 255px !important;
    }

    .access-card-note {
        min-height: 10.8rem !important;
    }

    div[data-testid="column"]:has(.access-card-content),
    div[data-testid="stColumn"]:has(.access-card-content),
    div[class*="stColumn"]:has(.access-card-content),
    div[class*="stVerticalBlockBorderWrapper"]:has(.access-card-content) {
        border: 2.5px solid #000000 !important;
        background-color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15) !important;
        padding: 1.25rem 1.45rem !important;
        min-height: 292px !important;
        box-sizing: border-box !important;
    }

    div[data-testid="column"]:has(.access-card-content) .access-card-content,
    div[data-testid="stColumn"]:has(.access-card-content) .access-card-content,
    div[class*="stColumn"]:has(.access-card-content) .access-card-content {
        padding: 0 !important;
        background: transparent !important;
    }

    div[data-testid="column"]:has(.access-card-content) div.stButton > button,
    div[data-testid="stColumn"]:has(.access-card-content) div.stButton > button,
    div[class*="stColumn"]:has(.access-card-content) div.stButton > button {
        width: auto !important;
        min-width: 245px !important;
        margin-top: 0.4rem !important;
    }


    /* DISEÑO DE ACORDEONES EXPANDERS */
    div[data-testid="stExpander"], div[class*="stExpander"] {
        border: 2.5px solid #000000 !important;
        background-color: #ffffff !important;
        border-radius: 10px !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08) !important;
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
    }

    div[data-testid="stExpander"] summary, div[class*="stExpander"] summary {
        padding: 0.65rem 1.15rem !important;
        background-color: #ffffff !important;
        border-radius: 10px !important;
    }

    div[data-testid="stExpander"] summary p, div[class*="stExpander"] summary p {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }

    div[data-testid="stExpander"] summary svg, div[class*="stExpander"] summary svg {
        transform: scale(1.35) !important;
        fill: #0b73b7 !important;
    }

</style>
""", unsafe_allow_html=True)


# =========================
# ESTADO INICIAL
# =========================

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

if "etapa" not in st.session_state:
    st.session_state.etapa = "formulario"

if "modo_acceso" not in st.session_state:
    st.session_state.modo_acceso = None

if "pendiente_confirmacion" not in st.session_state:
    st.session_state.pendiente_confirmacion = False

if "ajuste_confirmacion" not in st.session_state:
    st.session_state.ajuste_confirmacion = False

if "tipo_ajuste_seleccionado" not in st.session_state:
    st.session_state.tipo_ajuste_seleccionado = "Modificar exposición total"


# =========================
# BASE DE DATOS
# =========================

df_herramientas = pd.read_csv("herramientas.csv")

if "origen" not in df_herramientas.columns:
    df_herramientas["origen"] = "Manual de instrucciones"

if "factor_correccion" not in df_herramientas.columns:
    df_herramientas["factor_correccion"] = 1.0


# =========================
# PDF
# =========================

def generar_pdf(titulo, resumen, filas_tabla, conclusion):
    nombre_pdf = "informe_vibraciones.pdf"

    doc = SimpleDocTemplate(
        nombre_pdf,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    estilos = getSampleStyleSheet()
    contenido = []
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    contenido.append(Paragraph("Informe de evaluación de vibraciones", estilos["Title"]))
    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph(f"Fecha de generación: {fecha}", estilos["Normal"]))
    contenido.append(Spacer(1, 18))

    contenido.append(Paragraph(titulo, estilos["Heading2"]))
    contenido.append(Paragraph(resumen, estilos["Normal"]))
    contenido.append(Spacer(1, 18))

    contenido.append(Paragraph("Resultados resumidos", estilos["Heading2"]))

    tabla = Table(
        filas_tabla,
        colWidths=[
            3.2 * cm,
            4.2 * cm,
            2.3 * cm,
            2.3 * cm,
            2.3 * cm,
            2.3 * cm
        ]
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
    ]))

    contenido.append(tabla)
    contenido.append(Spacer(1, 18))

    contenido.append(Paragraph("Conclusión / recomendación", estilos["Heading2"]))
    contenido.append(Paragraph(conclusion, estilos["Normal"]))

    doc.build(contenido)

    return nombre_pdf



def mostrar_dato(titulo, valor, clase="metric-normal"):
    st.markdown(
        f"""
        <div class="custom-metric {clase}">
            <div class="custom-metric-label">{titulo}</div>
            <div class="custom-metric-value">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_aviso(texto, tipo="warning"):
    clases = {
        "warning": "alert-warning-custom",
        "success": "alert-success-custom",
        "error": "alert-error-custom"
    }
    clase = clases.get(tipo, "alert-warning-custom")
    st.markdown(
        f'<div class="{clase}">{texto}</div>',
        unsafe_allow_html=True
    )


def mostrar_tabla_clara(df, height=240):
    html = df.to_html(index=False, escape=True, classes="tabla-clara")
    st.markdown(
        f'<div class="tabla-scroll" style="max-height:{height}px;">{html}</div>',
        unsafe_allow_html=True
    )


def obtener_color_por_puntos(puntos):
    """Devuelve color y texto según el nivel de puntos de exposición."""
    if puntos >= 400:
        return "#ff3b3b", "Supera el valor límite"
    elif puntos >= 100:
        return "#ff9800", "Supera el nivel de acción"
    else:
        return "#1fa324", "Nivel seguro"


def aplicar_color_slider(key_slider, color):
    """Colorea el punto por completo (sólido) y dibuja una única línea horizontal negra limpia."""
    st.markdown(
        f"""
        <style>
        /* 1. Punto del slider (completamente SÓLIDO y relleno con su color dinámico) */
        .st-key-{key_slider} [data-baseweb="slider"] [role="slider"] {{
            background-color: {color} !important;
            background: {color} !important;
            border: 2px solid {color} !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
            border-radius: 50% !important;
            width: 14px !important;
            height: 14px !important;
        }}

        /* 2. Número superior con el color de su estado */
        .st-key-{key_slider} [data-baseweb="slider"] [data-testid="stThumbValue"] {{
            color: {color} !important;
            font-weight: 800 !important;
        }}

        /* 3. Eliminación del bloque rojo activo y gris de fondo */
        .st-key-{key_slider} [data-baseweb="slider"] div {{
            background-image: none !important;
        }}
        
        /* Protegemos el fondo del punto usando :not([role="slider"]) */
        .st-key-{key_slider} [data-baseweb="slider"] > div:first-child div:not([role="slider"]) {{
            background: transparent !important;
            background-color: transparent !important;
        }}

        /* 4. Dibujar la línea negra continua de 2px en el carril principal */
        .st-key-{key_slider} [data-baseweb="slider"] > div:first-child {{
            background: linear-gradient(
                to bottom, 
                transparent calc(50% - 1px), 
                #000000 calc(50% - 1px), 
                #000000 calc(50% + 1px), 
                transparent calc(50% + 1px)
            ) !important;
            padding: 8px 0 !important;
        }}

        /* 5. Contenedor inferior de los números (0 y 147) 100% transparente */
        .st-key-{key_slider} [data-baseweb="slider"] > div:nth-child(2),
        .st-key-{key_slider} [data-baseweb="slider"] > div:nth-child(2) div {{
            background: transparent !important;
            background-color: transparent !important;
            background-image: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def guardar_y_calcular(tareas, tipo_vibracion, LIMITE, VLE):
    st.session_state["tareas_calculadas"] = tareas
    st.session_state["tipo_calculado"] = tipo_vibracion
    st.session_state["limite_calculado"] = LIMITE
    st.session_state["vle_calculado"] = VLE
    st.session_state.etapa = "resultado"
    st.rerun()


# =========================
# CÁLCULOS
# =========================

def calcular_puntos_mano_brazo(aceleracion, tiempo_horas):
    return ((aceleracion / 2.5) ** 2) * (tiempo_horas / 8) * 100


def calcular_puntos(tarea, tiempo=None):

    if tiempo is None:
        tiempo = tarea["t"]

    return calcular_puntos_mano_brazo(
        tarea["a"],
        tiempo
    )


def calcular_tiempo_para_puntos(tarea, puntos_objetivo):
    if puntos_objetivo <= 0:
        return 0

    puntos_actuales = calcular_puntos(tarea)

    if puntos_actuales <= 0:
        return 0

    return tarea["t"] * (puntos_objetivo / puntos_actuales)


def aplicar_objetivo_global(tareas, objetivo, LIMITE, VLE):
    tareas_ajustadas = []
    pasos_reduccion = []

    for tarea in tareas:
        nueva_tarea = tarea.copy()
        nueva_tarea["t_original"] = tarea["t"]
        nueva_tarea["puntos_originales"] = calcular_puntos(tarea)
        tareas_ajustadas.append(nueva_tarea)

    total_actual = sum(calcular_puntos(t) for t in tareas_ajustadas)

    if total_actual <= objetivo:
        return tareas_ajustadas, total_actual, pasos_reduccion

    # Factor común para que el total ajustado coincida con el objetivo seleccionado.
    # No se redondean los tiempos internamente; solo se redondean al mostrarlos.
    # Así evitamos desviaciones como 95.18 cuando el objetivo era 95.
    factor_reduccion = objetivo / total_actual

    for tarea in tareas_ajustadas:
        puntos_actuales = calcular_puntos(tarea)

        if puntos_actuales <= 0:
            continue

        tiempo_anterior = tarea["t"]
        puntos_anteriores = puntos_actuales

        nuevo_tiempo = tiempo_anterior * factor_reduccion
        tarea["t"] = nuevo_tiempo
        tarea["puntos_ajustados"] = calcular_puntos(tarea)

        pasos_reduccion.append(
            f"{tarea['nombre']} ({tarea['situacion']}): "
            f"{round(puntos_anteriores, 2)} puntos → "
            f"{round(tarea['puntos_ajustados'], 2)} puntos | "
            f"{round(tiempo_anterior, 2)} h → {round(tarea['t'], 2)} h"
        )

    nuevo_total = sum(calcular_puntos(t) for t in tareas_ajustadas)

    return tareas_ajustadas, nuevo_total, pasos_reduccion


# =========================
# MATRIZ OPTIMIZADA
# =========================

def crear_matriz_puntos(tareas, tipo_vibracion, vle, titulo):
    # Desplazamos la rejilla base horizontal a 0.1 con paso 0.5 para albergar tiempos cortos
    tiempos = np.arange(0.1, 8.6, 0.5)
    referencia = 2.5

    puntos_totales_previos = sum(calcular_puntos(t) for t in tareas)
    tiempo_total_previo = sum(t["t"] for t in tareas)

    aceleracion_total_equivalente = 0

    if tiempo_total_previo > 0:
        aceleracion_total_equivalente = basePath = referencia * np.sqrt(
            (puntos_totales_previos * 8) / (100 * tiempo_total_previo)
        )

    aceleracion_max_herramientas = max(
        [float(t["a"]) for t in tareas] + [10.0, aceleracion_total_equivalente]
    )

    aceleracion_max_grafico = np.ceil((aceleracion_max_herramientas + 1.0) * 2) / 2
    aceleraciones = np.arange(1, aceleracion_max_grafico + 0.5, 0.5)

    z = []

    for a in aceleraciones:
        fila = []
        for t in tiempos:
            puntos = ((a / referencia) ** 2) * (t / 8) * 100
            fila.append(round(puntos, 0))
        z.append(fila)

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        x=tiempos,
        y=aceleraciones,
        z=z,
        text=z,
        texttemplate="%{text:.0f}",
        textfont={"size": 8, "color": "black"},
        colorscale=[
            [0.0, "#1fa324"],
            [0.25, "#8ee35f"],
            [0.50, "#fff000"],
            [0.75, "#ff8c1a"],
            [1.0, "#ff1e1e"]
        ],
        zmin=0,
        zmax=vle,
        showscale=False,
        hovertemplate="Tiempo: %{x} h<br>Aceleración: %{y} m/s²<br>Puntos: %{z}<extra></extra>"
    ))

    puntos_totales = 0
    tiempo_total = 0

    for tarea in tareas:
        puntos = calcular_puntos(tarea)
        puntos_totales += puntos
        tiempo_total += tarea["t"]

        aceleracion_visual = tarea["a"]
        nombre_corto = tarea["nombre"]

        if len(nombre_corto) > 18:
            nombre_corto = nombre_corto[:18] + "..."

        texto_point = f"{nombre_corto}<br>{round(puntos, 0)} p"

        fig.add_trace(go.Scatter(
            x=[tarea["t"]],
            y=[aceleracion_visual],
            mode="markers+text",
            marker=dict(
                size=16,
                color="#2455ff",
                line=dict(width=2, color="white")
            ),
            text=[texto_point],
            textposition="top right", 
            textfont=dict(size=10, color="#085283"), # Modificación: Texto de herramientas en azul legible
            cliponaxis=False,
            name=tarea["nombre"],
            showlegend=False,
            hovertemplate=(
                f"{tarea['nombre']}<br>"
                f"Situación: {tarea['situacion']}<br>"
                f"Tiempo: {tarea['t']} h<br>"
                f"Aceleración corregida: {round(tarea['a'], 2)} m/s²<br>"
                f"Puntos: {round(puntos, 1)}"
                "<extra></extra>"
            )
        ))

    if tiempo_total > 0:
        aceleracion_equivalente = referencia * np.sqrt(
            (puntos_totales * 8) / (100 * tiempo_total)
        )

        fig.add_trace(go.Scatter(
            x=[tiempo_total],
            y=[aceleracion_equivalente],
            mode="markers+text",
            marker=dict(size=28, color="black", line=dict(width=4, color="white")),
            text=[f"TOTAL<br>{round(puntos_totales, 1)} p"],
            textposition="bottom right",
            textfont=dict(size=11, color="#085283"), # Modificación: Texto de la puntuación TOTAL en azul legible
            cliponaxis=False,
            name="Total",
            showlegend=False,
            hovertemplate=f"Total combinado: {round(puntos_totales, 1)} puntos<extra></extra>"
        ))

    fig.update_layout(
        title=dict(
            text=titulo,
            x=0.5,
            xanchor="center",
            font=dict(color="black", size=18)
        ),
        xaxis_title="Tiempo de exposición (h)",
        yaxis_title="Aceleración corregida (m/s²)",
        width=950,
        height=430,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=11, color="black"),
        margin=dict(l=45, r=50, t=50, b=40)
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], 
        tickfont=dict(color="black"),
        title_font=dict(color="black"),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.15)",
        linecolor="black",
        zerolinecolor="black",
        range=[0, 8.5] 
    )

    fig.update_yaxes(
        tickfont=dict(color="black"),
        title_font=dict(color="black"),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.15)",
        linecolor="black",
        zerolinecolor="black",
        range=[0, aceleracion_max_grafico]
    )

    return fig


# =========================
# LEYENDA
# =========================

def mostrar_leyenda(tipo_vibracion, vle):
    texto_vle = "400"

    st.markdown("#### Leyenda")
    st.markdown("**Nivel de riesgo**")

    st.html(f"""
<div style="font-size:13px; line-height:1.35;">
    <div style="display:flex; align-items:center; margin-bottom:12px;">
        <div style="background:#1fa324; width:34px; height:18px; margin-right:12px;"></div>
        <span>0 - 100 · Nivel seguro</span>
    </div>

    <div style="display:flex; align-items:center; margin-bottom:12px;">
        <div style="background:#ff8c1a; width:34px; height:18px; margin-right:12px;"></div>
        <span>100 - {texto_vle} · Nivel de acción</span>
    </div>

    <div style="display:flex; align-items:center; margin-bottom:16px;">
        <div style="background:#ff1e1e; width:34px; height:18px; margin-right:12px;"></div>
        <span>&gt; {texto_vle} · Superación valor límite</span>
    </div>
</div>
""")

    st.divider()
    st.markdown("**Puntos**")

    st.html("""
<div style="font-size:13px; line-height:1.35;">
    <div style="display:flex; align-items:center; margin-bottom:12px;">
        <div style="background:#2455ff; width:20px; height:20px; border-radius:50%; margin-right:12px; border:2px solid white; box-shadow:0 0 0 1px #777;"></div>
        <span>Herramientas</span>
    </div>

    <div style="display:flex; align-items:center; margin-bottom:8px;">
        <div style="background:black; width:22px; height:22px; border-radius:50%; margin-right:12px; border:2px solid white; box-shadow:0 0 0 1px #777;"></div>
        <span>Puntos totales</span>
    </div>
</div>
""")


def mostrar_matriz_con_leyenda(fig, tipo_vibracion, vle):
    # La matriz se muestra con ancho fijo para que no ocupe toda la pantalla.
    # Las columnas laterales ayudan a centrar el bloque gráfico + leyenda.
    col_izq, col_matriz, col_leyenda, col_der = st.columns([0.25, 3.9, 1.25, 0.25])

    with col_matriz:
        st.plotly_chart(fig, use_container_width=False)

    with col_leyenda:
        with st.container(border=True):
            mostrar_leyenda(tipo_vibracion, vle)

    mostrar_aviso(
        "Interpretación: las zonas verdes representan exposiciones seguras, "
        "las naranjas indican superación del nivel de acción y las rojas "
        "indican superación del valor límite.",
        "success"
    )


# =========================
# INTERFAZ PRINCIPAL
# =========================

st.markdown(
    '<div class="main-title">EVALUACIÓN DE EXPOSICIÓN A VIBRACIONES MANO-BRAZO</div>',
    unsafe_allow_html=True
)


# =========================
# SELECCIÓN DE MODO
# =========================

if st.session_state.modo_acceso is None:

    st.markdown('<div class="access-heading">Selecciona modo de acceso</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown(
                """
                <div class="access-card-content access-panel">
                    <div class="access-title">Trabajador</div>
                    <div class="access-text access-card-note">
                        Acceso para realizar una evaluación:<br><br>
                        • Seleccionar herramientas<br>
                        • Introducir tiempos de uso<br>
                        • Calcular exposición<br>
                        • Ajustar tiempos
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("ENTRAR COMO TRABAJADOR →", key="btn_acceso_trabajador"):
                st.session_state.modo_acceso = "trabajador"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown(
                """
                <div class="access-card-content access-panel">
                    <div class="access-title">Técnico de prevención</div>
                    <div class="access-text access-card-note">
                        Acceso para gestionar la base de datos:<br><br>
                        • Ver herramientas registradas<br>
                        • Añadir nuevos equipos<br>
                        • Mantener los datos actualizados<br>
                        • Revisar origen y fuente de los datos
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("ENTRAR COMO TÉCNICO →", key="btn_acceso_tecnico"):
                st.session_state.modo_acceso = "tecnico"
                st.rerun()

    st.stop()


col_reset_top, col_space_top, col_next_top = st.columns([1.0, 4.0, 2.2])

with col_reset_top:
    if st.button("🔄 Reiniciar", key="reiniciar_top"):
        st.session_state.clear()
        st.session_state.reset_counter = 0
        st.session_state.etapa = "formulario"
        st.session_state.modo_acceso = None
        st.rerun()

top_next_placeholder = col_next_top.empty()


# =========================
# PANEL TÉCNICO
# =========================

if st.session_state.modo_acceso == "tecnico":

    col_titulo_tecnico, col_cerrar_tecnico = st.columns([5.8, 1.2])

    with col_titulo_tecnico:
        st.title(" Panel técnico de prevención")

    with col_cerrar_tecnico:
        st.markdown("<div style='height: 0.45rem;'></div>", unsafe_allow_html=True)
        if st.button("Cerrar sesión", key="cerrar_sesion_tecnico_top"):
            st.session_state.clear()
            st.session_state.reset_counter = 0
            st.session_state.etapa = "formulario"
            st.session_state.modo_acceso = None
            st.rerun()

    if st.session_state.get("herramienta_guardada_ok", False):
        st.success("Herramienta guardada correctamente.")
        st.session_state.herramienta_guardada_ok = False

    if st.session_state.get("herramienta_eliminada_ok", False):
        st.success("Herramienta eliminada correctamente.")
        st.session_state.herramienta_eliminada_ok = False

    with st.expander("➕ Añadir nueva herramienta", expanded=False):

        st.markdown(
            '<p class="compact-text">Completa los datos de la nueva herramienta y pulsa <b>GUARDAR HERRAMIENTA</b>. '
            'Al guardarla, se incorporará automáticamente a la base de datos inferior.</p>',
            unsafe_allow_html=True
        )

        col_form1, col_form2 = st.columns(2)

        with col_form1:
            nueva_herramienta = st.text_input("Herramienta", key="nueva_herramienta")

        with col_form2:
            nueva_situacion = st.text_input("Situación", key="nueva_situacion")

        nuevo_tipo = "Mano-brazo"
        st.info("Todas las herramientas añadidas serán de tipo Mano-brazo")

        col_form3, col_form4, col_form5 = st.columns([1.2, 1.2, 2.0])

        with col_form3:
            nueva_aceleracion = st.number_input(
                "Aceleración (m/s²)",
                min_value=0.0,
                step=0.1,
                key="nueva_aceleracion"
            )

        with col_form4:
            nueva_incertidumbre = st.number_input(
                "Incertidumbre",
                min_value=0.0,
                step=0.1,
                key="nueva_incertidumbre"
            )

        with col_form5:
            nuevo_origen = st.selectbox(
                "Origen de los datos",
                [
                    "Manual de instrucciones",
                    "Base de datos",
                    "Medición propia"
                ],
                key="nuevo_origen"
            )

        if nuevo_origen == "Manual de instrucciones":
            aplicar_factor_correccion = st.checkbox(
                "Aplicar factor de corrección",
                value=False,
                key="aplicar_factor_correccion"
            )

            if aplicar_factor_correccion:
                col_factor, col_info_factor = st.columns([1.2, 3.5])

                with col_factor:
                    nuevo_factor_correccion = st.number_input(
                        "Factor de corrección",
                        min_value=0.0,
                        value=1.0,
                        step=0.1,
                        key="nuevo_factor_correccion"
                    )

                with col_info_factor:
                    st.info(
                        "Se aplicará factor de corrección. "
                        "Aceleración usada = (aceleración + incertidumbre) × factor de corrección."
                    )
            else:
                nuevo_factor_correccion = 1.0
                st.info(
                    "No se aplica factor de corrección. "
                    "Internamente se utilizará factor = 1."
                )
        else:
            aplicar_factor_correccion = False
            nuevo_factor_correccion = 1.0

        nueva_fuente = st.text_input("Fuente", key="nueva_fuente")

        col_guardar, col_guardar_espacio = st.columns([1.45, 5.0])
        with col_guardar:
            guardar = st.button("GUARDAR HERRAMIENTA", key="btn_guardar_herramienta")

        if guardar:
            if nueva_herramienta.strip() == "" or nueva_situacion.strip() == "" or nueva_fuente.strip() == "":
                st.warning("Completa herramienta, situación y fuente antes de guardar.")
            else:
                nueva_fila = {
                    "herramienta": nueva_herramienta,
                    "situacion": nueva_situacion,
                    "tipo": nuevo_tipo,
                    "aceleracion": nueva_aceleracion,
                    "incertidumbre": nueva_incertidumbre,
                    "factor_correccion": nuevo_factor_correccion,
                    "origen": nuevo_origen,
                    "fuente": nueva_fuente
                }

                df_herramientas.loc[len(df_herramientas)] = nueva_fila

                df_herramientas.to_csv(
                    "herramientas.csv",
                    index=False
                )

                st.session_state.herramienta_guardada_ok = True
                st.rerun()

    st.divider()

    with st.container(border=True):
        st.markdown("## Base de datos actual")
        mostrar_tabla_clara(df_herramientas, height=255)

    with st.expander("🗑️ Eliminar herramienta", expanded=False):
        if df_herramientas.empty:
            st.info("No hay herramientas registradas para eliminar.")
        else:
            st.markdown(
                '<p class="compact-text">Selecciona la herramienta que quieres eliminar de la base de datos y pulsa <b>ELIMINAR HERRAMIENTA</b>.</p>',
                unsafe_allow_html=True
            )

            indices_herramientas = df_herramientas.index.tolist()

            def formato_herramienta(indice):
                fila = df_herramientas.loc[indice]
                return f"{fila['herramienta']} · {fila['situacion']} · {fila['origen']}"

            indice_eliminar = st.selectbox(
                "Herramienta a eliminar",
                indices_herramientas,
                format_func=formato_herramienta,
                key="indice_herramienta_eliminar"
            )

            fila_eliminar = df_herramientas.loc[indice_eliminar]
            st.warning(
                f"Vas a eliminar: {fila_eliminar['herramienta']} · {fila_eliminar['situacion']}. "
                "Esta acción actualizará el archivo herramientas.csv."
            )

            col_eliminar, col_eliminar_espacio = st.columns([1.45, 5.0])
            with col_eliminar:
                if st.button("ELIMINAR HERRAMIENTA", key="btn_eliminar_herramienta"):
                    df_herramientas = df_herramientas.drop(indice_eliminar).reset_index(drop=True)
                    df_herramientas.to_csv("herramientas.csv", index=False)
                    st.session_state.herramienta_eliminada_ok = True
                    st.rerun()

    st.stop()


# =========================
# ETAPA 1: FORMULARIO
# =========================

if st.session_state.etapa == "formulario":

    tipo_vibracion = "Mano-brazo"
    LIMITE = 100
    VLE = 400

    if st.session_state.pendiente_confirmacion:
        with st.container(border=True):
            mostrar_aviso(
                "⚠️ **Aviso de datos incompletos:** No has introducido los tiempos de uso de las herramientas "
                "(el tiempo total es de 0 horas). ¿Estás seguro de que deseas continuar con la evaluación?",
                "warning"
            )
            col_c1, col_c2, _ = st.columns([1.5, 1.8, 4])
            with col_c1:
                if st.button("🔥 SÍ, CONTINUAR", key="confirmar_si_proceder"):
                    st.session_state.pendiente_confirmacion = False
                    guardar_y_calcular(st.session_state.tareas_temporales, tipo_vibracion, LIMITE, VLE)
            with col_c2:
                if st.button("❌ NO, VOLVER A REVISAR", key="confirmar_no_revisar"):
                    st.session_state.pendiente_confirmacion = False
                    st.rerun()
        st.divider()

    tab1, tab2 = st.tabs(["📋 1. Datos de exposición", "🛠️ 2. Herramientas utilizadas"])

    with tab1:
        with st.container(border=True):
            st.markdown("### Paso 1 · Datos de exposición")
            st.markdown(
                '<p class="compact-text">Evalúa la exposición a vibraciones mano-brazo según el tiempo de uso y la aceleración estimada de las herramientas.</p>',
                unsafe_allow_html=True
            )
            st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)

            col_info1, col_info2, col_info3 = st.columns(3)

            with col_info1:
                mostrar_dato("Tipo de vibración", "Mano-brazo")

            with col_info2:
                mostrar_dato("Nivel de acción", "100 puntos", "metric-action")

            with col_info3:
                mostrar_dato("Valor límite", "400 puntos", "metric-limit")
        
        st.info("💡 Una vez revisados los límites de referencia, haz clic arriba en la pestaña **'2. Herramientas utilizadas'** para completar los datos.")

    with tab2:
        df_filtrado = df_herramientas[df_herramientas["tipo"] == tipo_vibracion]

        if df_filtrado.empty:
            st.error("No hay herramientas registradas para este tipo de vibración en herramientas.csv.")
            st.stop()

        with st.container(border=True):
            st.markdown("### Paso 2 · Herramientas utilizadas")
            col_cant_herramientas, _ = st.columns([1.5, 3.5])
            with col_cant_herramientas:
                num_tareas = st.number_input(
                    "¿Cuántas herramientas o equipos vas a utilizar?",
                    min_value=1,
                    step=1,
                    key=f"num_tareas_{st.session_state.reset_counter}"
                )

        st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)

        tareas = []

        for i in range(num_tareas):
            with st.container(border=True):
                st.markdown(f"#### Operación {i + 1}")
                herramientas_disponibles = df_filtrado["herramienta"].unique().tolist()

                col1, col2, col3 = st.columns([2, 2, 1.2])

                with col1:
                    herramienta = st.selectbox(
                        f"Herramienta/equipo {i + 1}",
                        herramientas_disponibles,
                        key=f"herramienta_{i}_{st.session_state.reset_counter}"
                    )

                situaciones_disponibles = df_filtrado[
                    df_filtrado["herramienta"] == herramienta
                ]["situacion"].unique().tolist()

                with col2:
                    situacion = st.selectbox(
                        f"Situación de uso {i + 1}",
                        situaciones_disponibles,
                        key=f"situacion_{i}_{st.session_state.reset_counter}"
                    )

                datos_herramienta = df_filtrado[
                    (df_filtrado["herramienta"] == herramienta) &
                    (df_filtrado["situacion"] == situacion)
                ].iloc[0]

                aceleracion = float(datos_herramienta["aceleracion"])
                incertidumbre = float(datos_herramienta["incertidumbre"])

                if "origen" in datos_herramienta.index:
                    origen_dato = str(datos_herramienta["origen"])
                else:
                    origen_dato = "Manual de instrucciones"

                if origen_dato == "Manual de instrucciones":
                    if "factor_correccion" in datos_herramienta.index:
                        factor_correccion = float(datos_herramienta["factor_correccion"])
                    else:
                        factor_correccion = 1.0
                    factor_correccion_mostrar = round(factor_correccion, 2)
                else:
                    factor_correccion = 1.0
                    factor_correccion_mostrar = "No aplica"

                fuente = str(datos_herramienta["fuente"])
                aceleracion_usada = (aceleracion + incertidumbre) * factor_correccion

                with col3:
                    tiempo = st.number_input(
                        f"Tiempo de uso (horas)",
                        min_value=0.0,
                        step=0.1,
                        key=f"tiempo_{i}_{st.session_state.reset_counter}"
                    )

                eje = "-"

                tareas.append({
                    "nombre": herramienta,
                    "situacion": situacion,
                    "a_declarada": aceleracion,
                    "incertidumbre": incertidumbre,
                    "origen": origen_dato,
                    "factor_correccion": factor_correccion,
                    "factor_correccion_mostrar": factor_correccion_mostrar,
                    "a": aceleracion_usada,
                    "fuente": fuente,
                    "t": tiempo,
                    "tipo": tipo_vibracion,
                    "eje": eje,
                    "k": factor_correccion
                })

        st.divider()

        with top_next_placeholder.container():
            if st.button("SIGUIENTE → CALCULAR EXPOSICIÓN", key="siguiente_arriba"):
                total_tiempo = sum(t["t"] for t in tareas)
                if total_tiempo == 0.0:
                    st.session_state.tareas_temporales = tareas
                    st.session_state.pendiente_confirmacion = True
                    st.rerun()
                else:
                    guardar_y_calcular(tareas, tipo_vibracion, LIMITE, VLE)

        if num_tareas > 1:
            col_btn_bottom, col_btn_space = st.columns([1.55, 5])
            with col_btn_bottom:
                if st.button("SIGUIENTE → CALCULAR EXPOSICIÓN", key="siguiente_abajo"):
                    total_tiempo = sum(t["t"] for t in tareas)
                    if total_tiempo == 0.0:
                        st.session_state.tareas_temporales = tareas
                        st.session_state.pendiente_confirmacion = True
                        st.rerun()
                    else:
                        guardar_y_calcular(tareas, tipo_vibracion, LIMITE, VLE)



# =========================
# ETAPA 2: RESULTADO INICIAL
# =========================

elif st.session_state.etapa == "resultado":

    tareas = st.session_state["tareas_calculadas"]
    tipo_vibracion = st.session_state["tipo_calculado"]
    LIMITE = st.session_state["limite_calculado"]
    VLE = st.session_state["vle_calculado"]

    with st.container(border=True):

        st.markdown("### Resultado inicial")

        puntos_totales = 0

        filas_tabla = [[
            "Herramienta/equipo",
            "Situación",
            "Tipo",
            "Eje",
            "Aceleración",
            "Incertidumbre",
            "Factor corrección",
            "Aceleración corregida",
            "Tiempo inicial (h)",
            "Puntos iniciales"
        ]]

        filas_resumen = []

        for tarea in tareas:
            puntos = calcular_puntos(tarea)
            puntos_totales += puntos

            filas_tabla.append([
                tarea["nombre"],
                tarea["situacion"],
                tarea["tipo"],
                tarea["eje"],
                str(tarea["a_declarada"]),
                str(tarea["incertidumbre"]),
                str(tarea.get("factor_correccion_mostrar", tarea["factor_correccion"])),
                str(round(tarea["a"], 2)),
                str(round(tarea["t"], 2)),
                str(round(puntos, 2))
            ])

            filas_resumen.append({
                "Herramienta": tarea["nombre"],
                "Situación": tarea["situacion"],
                "Tiempo (h)": tarea["t"],
                "Aceleración (m/s²)": tarea["a_declarada"],
                "Incertidumbre": tarea["incertidumbre"],
                "Factor corrección": tarea.get("factor_correccion_mostrar", tarea["factor_correccion"]),
                "Aceleración corregida (m/s²)": round(tarea["a"], 2),
                "Puntos": round(puntos, 2)
            })

        st.session_state["filas_tabla"] = filas_tabla
        st.session_state["puntos_totales"] = puntos_totales

        col_res1, col_res2, col_res3 = st.columns(3)

        with col_res1:
            mostrar_dato("Puntos totales", round(puntos_totales, 2))

        with col_res2:
            mostrar_dato("Nivel de acción", LIMITE, "metric-action")

        with col_res3:
            mostrar_dato("VLE", VLE, "metric-limit")

        if puntos_totales >= VLE:
            mostrar_aviso("Resultado inicial: se supera el valor límite de exposición.", "error")
            estado = "Se supera el valor límite de exposición (VLE)."
        elif puntos_totales >= LIMITE:
            mostrar_aviso("Resultado inicial: se supera el nivel de acción.", "warning")
            estado = "Se supera el nivel de acción."
        else:
            mostrar_aviso("Resultado inicial: nivel seguro.", "success")
            estado = "Nivel seguro."

        st.session_state["estado"] = estado

    st.divider()

    with st.expander("📋 Ver desglose por herramienta"):

        df_resumen = pd.DataFrame(filas_resumen)

        mostrar_tabla_clara(
            df_resumen,
            height=min(260, 80 + 35 * len(df_resumen))
        )

    st.divider()

    with st.expander("📊 Ver matriz inicial de exposición"):

        fig_inicial = crear_matriz_puntos(
            tareas,
            tipo_vibracion,
            VLE,
            "Matriz inicial de puntuaciones"
        )

        mostrar_matriz_con_leyenda(fig_inicial, tipo_vibracion, VLE)

    st.divider()

    col_anterior, col_espacio, col_ajustar = st.columns([1.3, 5.8, 1.8])

    with col_anterior:
        if st.button("← ANTERIOR", key="btn_anterior_resultado"):
            st.session_state.etapa = "formulario"
            st.rerun()

    with col_ajustar:
        if st.button("AJUSTAR EXPOSICIÓN →", key="btn_ajustar_resultado"):
            st.session_state.etapa = "ajuste"
            st.session_state.ajuste_confirmacion = False  
            st.rerun()


# =========================
# ETAPA 3: AJUSTE DE EXPOSICIÓN (CON FLUJO SECUENCIAL)
# =========================

elif st.session_state.etapa == "ajuste":

    tareas = st.session_state["tareas_calculadas"]
    tipo_vibracion = st.session_state["tipo_calculado"]
    LIMITE = st.session_state["limite_calculado"]
    VLE = st.session_state["vle_calculado"]
    puntos_totales = st.session_state["puntos_totales"]

    if not st.session_state.ajuste_confirmacion:
        with st.container(border=True):
            st.markdown("### Ajuste de exposición")
            st.markdown("""
            Selecciona cómo quieres modificar la exposición:

            - **Modificar exposición total**: la aplicación reparte la reducción entre todas las herramientas según su contribución al total.
            - **Modificar herramienta individual**: puedes ajustar manualmente los puntos de cada herramienta y ver cómo cambia el total.
            """)

            tipo_ajuste = st.radio(
                "Tipo de ajuste",
                [
                    "Modificar exposición total",
                    "Modificar herramienta individual"
                ],
                horizontal=True
            )

            st.divider()

            col_anterior, col_espacio, col_configurar = st.columns([1.3, 5.5, 2.2])
            with col_anterior:
                if st.button("← ANTERIOR", key="btn_regresar_a_paso3"):
                    st.session_state.etapa = "resultado"
                    st.rerun()
            with col_configurar:
                if st.button("CONFIGURAR AJUSTE DE TIEMPOS →", key="btn_confirmar_seleccion_metodo"):
                    st.session_state.tipo_ajuste_seleccionado = tipo_ajuste
                    st.session_state.ajuste_confirmacion = True
                    st.rerun()

    else:
        if st.session_state.tipo_ajuste_seleccionado == "Modificar exposición total":
            with st.container(border=True):
                st.markdown("### Ajuste por exposición total")
                st.markdown("""
                Selecciona el objetivo de puntos totales.  
                La reducción se aplicará proporcionalmente según el peso de cada herramienta en el total.
                """)

                valor_slider_total = st.session_state.get(
                    "slider_objetivo",
                    int(round(puntos_totales))
                )
                color_slider_total, _ = obtener_color_por_puntos(valor_slider_total)
                aplicar_color_slider("slider_objetivo", color_slider_total)

                objetivo = st.slider(
                    "Objetivo de puntos totales",
                    min_value=0,
                    max_value=max(int(round(puntos_totales)), 1),
                    value=max(int(round(puntos_totales)), 0), 
                    step=1,
                    key="slider_objetivo"
                )

                col_m1, col_m2, col_m3 = st.columns(3)

                with col_m1:
                    mostrar_dato("Total inicial", round(puntos_totales, 2))

                with col_m2:
                    mostrar_dato("Objetivo seleccionado", objetivo)

                with col_m3:
                    diferencia = puntos_totales - objetivo
                    mostrar_dato("Reducción necesaria", round(diferencia, 2), "metric-action")

                st.divider()

                col_anterior, col_espacio, col_aplicar = st.columns([1.3, 5.8, 1.7])
                with col_anterior:
                    if st.button("← ANTERIOR", key="btn_ant_total_inner"):
                        st.session_state.ajuste_confirmacion = False  
                        st.rerun()

                with col_aplicar:
                    if st.button("APLICAR AJUSTE →", key="btn_apli_total_inner"):
                        tareas_ajustadas, nuevo_total, pasos_reduccion = aplicar_objetivo_global(
                            tareas,
                            objetivo,
                            LIMITE,
                            VLE
                        )
                        st.session_state["pasos_reduccion"] = pasos_reduccion
                        st.session_state["objetivo"] = objetivo
                        st.session_state["tareas_ajustadas"] = tareas_ajustadas
                        st.session_state["nuevo_total"] = nuevo_total
                        st.session_state.etapa = "ajustada"
                        st.rerun()

        else:
            with st.container(border=True):
                st.markdown("### Ajuste por herramienta individual")
                st.markdown("""
                Modifica los puntos objetivo de cada herramienta.  
                El total se recalcula teniendo en cuenta todos los cambios realizados.
                """)

                tareas_individuales = []
                nuevo_total_individual = 0
                pasos_individuales = []

                for i, tarea in enumerate(tareas):
                    puntos_actuales = calcular_puntos(tarea)
                    key_slider = f"slider_individual_{i}"

                    valor_slider_actual = st.session_state.get(
                        key_slider,
                        int(round(puntos_actuales))
                    )
                    color_slider, _ = obtener_color_por_puntos(valor_slider_actual)
                    aplicar_color_slider(key_slider, color_slider)


                    objetivo_herramienta = st.slider(
                        f"{tarea['nombre']} · {tarea['situacion']}",
                        min_value=0,
                        max_value=max(int(round(puntos_actuales * 1.5)), 1),
                        value=int(round(puntos_actuales)),
                        step=1,
                        key=key_slider
                    )

                    if puntos_actuales > 0:
                        nuevo_tiempo = tarea["t"] * (objetivo_herramienta / puntos_actuales)
                    else:
                        nuevo_tiempo = 0

                    nueva_tarea = tarea.copy()
                    nueva_tarea["t_original"] = tarea["t"]
                    nueva_tarea["puntos_originales"] = puntos_actuales
                    nueva_tarea["t"] = nuevo_tiempo
                    nueva_tarea["puntos_ajustados"] = calcular_puntos(nueva_tarea)

                    nuevo_total_individual += nueva_tarea["puntos_ajustados"]
                    tareas_individuales.append(nueva_tarea)

                    pasos_individuales.append(
                        f"{tarea['nombre']} ({tarea['situacion']}): "
                        f"{round(puntos_actuales, 2)} puntos → "
                        f"{round(nueva_tarea['puntos_ajustados'], 2)} puntos | "
                        f"{round(tarea['t'], 2)} h → {round(nueva_tarea['t'], 2)} h"
                    )

                st.divider()

                col_i1, col_i2, col_i3 = st.columns(3)

                with col_i1:
                    mostrar_dato("Total inicial", round(puntos_totales, 2))

                with col_i2:
                    mostrar_dato("Nuevo total estimado", round(nuevo_total_individual, 2))

                with col_i3:
                    mostrar_dato(
                        "Diferencia",
                        round(nuevo_total_individual - puntos_totales, 2),
                        "metric-action"
                    )

                if nuevo_total_individual >= VLE:
                    mostrar_aviso("Con estos ajustes se supera el VLE.", "error")
                elif nuevo_total_individual >= LIMITE:
                    mostrar_aviso("Con estos ajustes se supera el nivel de acción.", "warning")
                else:
                    mostrar_aviso("Con estos ajustes no se supera el nivel de acción.", "success")

            st.divider()

            with st.container(border=True):
                st.markdown("### Resumen de tiempos ajustados")
                filas_individuales = []

                for tarea in tareas_individuales:
                    diferencia_tiempo = tarea["t"] - tarea["t_original"]
                    filas_individuales.append({
                        "Herramienta": tarea["nombre"],
                        "Situación": tarea["situacion"],
                        "Puntos iniciales": round(tarea["puntos_originales"], 2),
                        "Puntos ajustados": round(tarea["puntos_ajustados"], 2),
                        "Tiempo inicial (h)": tarea["t_original"],
                        "Tiempo ajustado (h)": round(tarea["t"], 2),
                        "Diferencia (h)": round(diferencia_tiempo, 2)
                    })

                df_individual = pd.DataFrame(filas_individuales)
                mostrar_tabla_clara(df_individual, height=min(260, 80 + 35 * len(df_individual)))

            st.divider()

            col_anterior, col_espacio, col_aplicar = st.columns([1.3, 5.3, 2.3])
            with col_anterior:
                if st.button("← ANTERIOR", key="btn_ant_indiv_inner"):
                    st.session_state.ajuste_confirmacion = False  
                    st.rerun()

            with col_aplicar:
                if st.button("APLICAR AJUSTE INDIVIDUAL →", key="btn_apli_indiv_inner"):
                    st.session_state["pasos_reduccion"] = pasos_individuales
                    st.session_state["objetivo"] = round(nuevo_total_individual, 2)
                    st.session_state["tareas_ajustadas"] = tareas_individuales
                    st.session_state["nuevo_total"] = nuevo_total_individual
                    st.session_state.etapa = "ajustada"
                    st.rerun()


# =========================
# ETAPA 4: RESULTADO AJUSTADO
# =========================

elif st.session_state.etapa == "ajustada":

    tareas = st.session_state["tareas_calculadas"]
    tareas_ajustadas = st.session_state["tareas_ajustadas"]
    tipo_vibracion = st.session_state["tipo_calculado"]
    LIMITE = st.session_state["limite_calculado"]
    VLE = st.session_state["vle_calculado"]
    objetivo = st.session_state["objetivo"]
    nuevo_total = st.session_state["nuevo_total"]
    puntos_totales = st.session_state["puntos_totales"]
    estado = st.session_state["estado"]
    filas_tabla = st.session_state["filas_tabla"]

    with st.container(border=True):

        st.markdown("### Resultado ajustado")

        col_a1, col_a2, col_a3 = st.columns(3)

        with col_a1:
            mostrar_dato("Objetivo seleccionado", objetivo)

        with col_a2:
            mostrar_dato("Total inicial", round(puntos_totales, 2), "metric-action")

        with col_a3:
            mostrar_dato("Total ajustado", round(nuevo_total, 2))

        if nuevo_total >= VLE:
            mostrar_aviso("Con el ajuste seleccionado se supera el VLE.", "error")
        elif nuevo_total >= LIMITE:
            mostrar_aviso("Con el ajuste seleccionado se supera el nivel de acción.", "warning")
        else:
            mostrar_aviso("Con el ajuste seleccionado no se supera el nivel de acción.", "success")

    filas_tabla_ajustada = [[
        "Herramienta/equipo",
        "Situación",
        "Tiempo inicial (h)",
        "Tiempo ajustado (h)",
        "Puntos ajustados"
    ]]

    filas_ajustadas_resumen = []

    for tarea in tareas_ajustadas:
        puntos_ajustados = calcular_puntos(tarea)

        filas_ajustadas_resumen.append({
            "Herramienta": tarea["nombre"],
            "Situación": tarea["situacion"],
            "Tiempo inicial (h)": tarea["t_original"],
            "Tiempo ajustado (h)": round(tarea["t"], 2),
            "Puntos ajustados": round(puntos_ajustados, 2)
        })

        filas_tabla_ajustada.append([
            tarea["nombre"],
            tarea["situacion"],
            str(tarea["t_original"]),
            str(round(tarea["t"], 2)),
            str(round(puntos_ajustados, 2))
        ])

    df_ajustado = pd.DataFrame(filas_ajustadas_resumen)

    st.divider()

    with st.expander("🕒 Ver nuevos tiempos propuestos"):
        mostrar_tabla_clara(
            df_ajustado,
            height=min(220, 75 + 35 * len(df_ajustado))
        )

    with st.expander("🔎 Ver proceso de reducción aplicado"):
        for paso in st.session_state["pasos_reduccion"]:
            st.write(paso)

    with st.expander("📊 Ver matriz ajustada"):
        fig_ajustada = crear_matriz_puntos(
            tareas_ajustadas,
            tipo_vibracion,
            VLE,
            "Matriz ajustada según el objetivo seleccionado"
        )

        mostrar_matriz_con_leyenda(fig_ajustada, tipo_vibracion, VLE)

    st.divider()

    resumen_pdf = (
        f"Tipo de vibración evaluada: {tipo_vibracion}. "
        f"Total inicial: {round(puntos_totales, 2)} puntos. "
        f"Total ajustado: {round(nuevo_total, 2)} puntos. "
        f"{estado}"
    )

    conclusion_pdf = (
        f"Objetivo seleccionado: {objetivo} puntos. "
        f"El sistema propone reducir los tiempos de uso mediante una reducción proporcional "
        f"según la contribución de cada herramienta al total, hasta obtener "
        f"{round(nuevo_total, 2)} puntos."
    )

    filas_pdf = [[
        "Herramienta",
        "Situación",
        "Tiempo inicial (h)",
        "Tiempo ajustado (h)",
        "Puntos iniciales",
        "Puntos ajustados"
    ]]

    for tarea in tareas_ajustadas:
        puntos_iniciales = tarea["puntos_originales"]
        puntos_ajustados = calcular_puntos(tarea)

        filas_pdf.append([
            tarea["nombre"],
            tarea["situacion"],
            str(tarea["t_original"]),
            str(round(tarea["t"], 2)),
            str(round(puntos_iniciales, 2)),
            str(round(puntos_ajustados, 2))
        ])

    pdf = generar_pdf(
        "Resultado de evaluación",
        resumen_pdf,
        filas_pdf,
        conclusion_pdf
    )

    col_anterior, col_descarga, col_nueva = st.columns([1.35, 2.2, 1.7])

    with col_anterior:
        if st.button("← ANTERIOR", key="btn_ant_final"):
            st.session_state.etapa = "ajuste"
            st.session_state.ajuste_confirmacion = True  
            st.rerun()

    with col_descarga:
        with open(pdf, "rb") as file:
            st.download_button(
                label="📄 DESCARGAR INFORME EN PDF",
                data=file,
                file_name="informe_vibraciones.pdf",
                mime="application/pdf"
            )

    with col_nueva:
        if st.button("NUEVA EVALUACIÓN", key="btn_nueva_evaluacion_final"):
            st.session_state.clear()
            st.session_state.reset_counter = 0
            st.session_state.etapa = "formulario"
            st.session_state.modo_acceso = None
            st.rerun()
