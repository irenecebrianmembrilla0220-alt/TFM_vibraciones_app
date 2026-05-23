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

st.markdown("""
<style>
    /* Pantalla más equilibrada: mantiene el estilo original sin apelotonar */
    .block-container {
        padding-top: 1.55rem !important;
        padding-bottom: 1.0rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        max-width: 100% !important;
    }

    .main-title {
        background-color: #0b73b7;
        color: white;
        padding: 22px 18px;
        text-align: center;
        border-radius: 6px;
        font-size: 25px;
        font-weight: bold;
        letter-spacing: 5px;
        margin-bottom: 22px;
        width: 100%;
        box-sizing: border-box;
        line-height: 1.35;
        min-height: 76px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: visible;
    }

    .step-box {
        background-color: #f7f7f7;
        border: 1px solid #dddddd;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
    }

    .section-title {
        color: #0b73b7;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Títulos algo más contenidos para que cada paso entre mejor en pantalla */
    h1 {
        font-size: 1.5rem !important;
        margin-bottom: 0.55rem !important;
    }

    h2 {
        font-size: 1.12rem !important;
        margin-bottom: 0.5rem !important;
    }

    h3 {
        font-size: 1.12rem !important;
        margin-bottom: 0.45rem !important;
    }

    h4 {
        font-size: 0.96rem !important;
        margin-bottom: 0.35rem !important;
    }

    p, li, label, .stMarkdown {
        font-size: 0.86rem !important;
    }

    /* Reduce un poco la altura de los selectores y number_input sin comprimirlos demasiado */
    div[data-baseweb="select"] > div {
        min-height: 2.18rem !important;
    }

    div[data-testid="stNumberInput"] input {
        min-height: 2.18rem !important;
        font-size: 0.86rem !important;
    }

    div.stButton > button {
        background-color: #0b73b7;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        height: 2.3em;
        width: 100%;
        border: none;
        padding: 0.25rem 0.8rem;
        font-size: 0.88rem;
    }

    div.stButton > button:hover {
        background-color: #095f96;
        color: white;
    }

    /* Métricas personalizadas: visibles, pero menos grandes que st.metric */
    .custom-metric {
        margin-top: 6px;
        margin-bottom: 8px;
        padding-top: 3px;
    }

    .custom-metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        line-height: 1.2;
        margin-bottom: 0.3rem;
    }

    .custom-metric-value {
        font-size: 1.75rem;
        font-weight: 500;
        line-height: 1.15;
    }

    .metric-normal {
        color: inherit;
    }

    .metric-action {
        color: #f39c12;
    }

    .metric-limit {
        color: #e74c3c;
    }

    hr {
        margin-top: 0.55rem !important;
        margin-bottom: 0.55rem !important;
    }


    /* Compactar Paso 2 y formularios sin perder legibilidad */
    div[data-testid="stVerticalBlock"] {
        gap: 0.45rem !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0.65rem !important;
    }

    div[data-testid="stNumberInput"] {
        margin-bottom: 0.15rem !important;
    }

    div[data-testid="stSelectbox"] {
        margin-bottom: 0.15rem !important;
    }

    div[data-testid="stNumberInput"] button {
        min-height: 2.18rem !important;
        height: 2.18rem !important;
    }

    .stSelectbox label,
    .stNumberInput label {
        font-size: 0.84rem !important;
        margin-bottom: 0.10rem !important;
    }

    .compact-text {
        font-size: 0.84rem !important;
        line-height: 1.15 !important;
        margin-bottom: 0.25rem !important;
    }


    .access-title {
        font-size: 1.10rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }

    .access-text {
        font-size: 0.92rem;
        line-height: 1.55;
        margin-bottom: 0.65rem;
    }

    .access-spacer {
        height: 1.75rem;
    }

    .access-card-note {
        min-height: 8.4rem;
    }


    a.anchor-link, .anchor-link {
        display: none !important;
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


# =========================
# BASE DE DATOS
# =========================

df_herramientas = pd.read_csv("herramientas.csv")

if "origen" not in df_herramientas.columns:
    df_herramientas["origen"] = "Manual de instrucciones"


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

    reduccion_necesaria = total_actual - objetivo

    for tarea in tareas_ajustadas:
        puntos_actuales = calcular_puntos(tarea)

        if puntos_actuales <= 0:
            continue

        peso = puntos_actuales / total_actual
        reduccion_herramienta = reduccion_necesaria * peso
        puntos_destino = puntos_actuales - reduccion_herramienta

        tiempo_anterior = tarea["t"]
        puntos_anteriores = puntos_actuales

        nuevo_tiempo = calcular_tiempo_para_puntos(tarea, puntos_destino)

        tarea["t"] = round(nuevo_tiempo, 2)
        tarea["puntos_ajustados"] = calcular_puntos(tarea)

        pasos_reduccion.append(
            f"{tarea['nombre']} ({tarea['situacion']}): "
            f"{round(puntos_anteriores, 2)} puntos → "
            f"{round(tarea['puntos_ajustados'], 2)} puntos | "
            f"{tiempo_anterior} h → {tarea['t']} h"
        )

    nuevo_total = sum(calcular_puntos(t) for t in tareas_ajustadas)

    return tareas_ajustadas, nuevo_total, pasos_reduccion


# =========================
# MATRIZ
# =========================

def crear_matriz_puntos(tareas, tipo_vibracion, vle, titulo):
    tiempos = np.arange(0.5, 8.5, 0.5)

    referencia = 2.5
    # La matriz se limita hasta 9.5 m/s² para que el máximo sea aproximadamente 1450 puntos
    # 9.5 m/s² durante 8 h equivale a 1444 puntos.
    aceleraciones = np.arange(1, 10.0, 0.5)

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

        texto_punto = f"{nombre_corto}<br>{round(puntos, 0)} p"

        fig.add_trace(go.Scatter(
            x=[tarea["t"]],
            y=[aceleracion_visual],
            mode="markers+text",
            marker=dict(
                size=16,
                color="#2455ff",
                line=dict(width=2, color="white")
            ),
            text=[texto_punto],
            textposition="top center",
            textfont=dict(size=10, color="black"),
            name=tarea["nombre"],
            showlegend=False,
            hovertemplate=(
                f"{tarea['nombre']}<br>"
                f"Situación: {tarea['situacion']}<br>"
                f"Tiempo: {tarea['t']} h<br>"
                f"Aceleración usada: {tarea['a']} m/s²<br>"
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
            textposition="bottom center",
            textfont=dict(size=11, color="black"),
            name="Total",
            showlegend=False,
            hovertemplate=f"Total combinado: {round(puntos_totales, 1)} puntos<extra></extra>"
        ))

    fig.update_layout(
        title=dict(
            text=titulo,
            x=0.5,
            xanchor="center",
            font=dict(color="black")
        ),
        xaxis_title="Tiempo de exposición (h)",
        yaxis_title="Aceleración equivalente (m/s²)",
        height=540,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12, color="black"),
        margin=dict(l=40, r=20, t=55, b=45)
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=list(tiempos),
        tickfont=dict(color="black"),
        title_font=dict(color="black"),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.15)",
        linecolor="black",
        zerolinecolor="black"
    )

    fig.update_yaxes(
        tickfont=dict(color="black"),
        title_font=dict(color="black"),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.15)",
        linecolor="black",
        zerolinecolor="black"
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
    col_matriz, col_leyenda = st.columns([4.5, 1.3])

    with col_matriz:
        st.plotly_chart(fig, use_container_width=True)

    with col_leyenda:
        with st.container(border=True):
            mostrar_leyenda(tipo_vibracion, vle)

    st.success(
        "Interpretación: las zonas verdes representan exposiciones seguras, "
        "las naranjas indican superación del nivel de acción y las rojas "
        "indican superación del valor límite."
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

    st.markdown("## Selecciona modo de acceso")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown(
                """
                <div class="access-title">Trabajador</div>
                <div class="access-text access-card-note">
                    Acceso para realizar una evaluación:<br><br>
                    • Seleccionar herramientas<br>
                    • Introducir tiempos de uso<br>
                    • Calcular exposición<br>
                    • Ajustar tiempos
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("ENTRAR COMO TRABAJADOR →"):
                st.session_state.modo_acceso = "trabajador"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown(
                """
                <div class="access-title">Técnico de prevención</div>
                <div class="access-text access-card-note">
                    Acceso para gestionar la base de datos:<br><br>
                    • Ver herramientas registradas<br>
                    • Añadir nuevos equipos<br>
                    • Mantener los datos actualizados<br>
                    • Revisar origen y fuente de los datos
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("ENTRAR COMO TÉCNICO →"):
                st.session_state.modo_acceso = "tecnico"
                st.rerun()

    st.stop()


if st.button("🔄 Reiniciar"):
    st.session_state.clear()
    st.session_state.reset_counter = 0
    st.session_state.etapa = "formulario"
    st.session_state.modo_acceso = None
    st.rerun()


# =========================
# PANEL TÉCNICO
# =========================

if st.session_state.modo_acceso == "tecnico":

    st.title("🧑‍💼 Panel técnico de prevención")

    with st.container(border=True):
        st.markdown("## Base de datos actual")

        st.dataframe(
            df_herramientas,
            use_container_width=True,
            height=360
        )

    st.divider()

    with st.container(border=True):

        st.markdown("## Añadir nueva herramienta")

        with st.form("form_nueva_herramienta"):

            nueva_herramienta = st.text_input("Herramienta")

            nueva_situacion = st.text_input("Situación")

            nuevo_tipo = "Mano-brazo"

            st.info("Todas las herramientas añadidas serán de tipo Mano-brazo")

            nueva_aceleracion = st.number_input(
                "Aceleración (m/s²)",
                min_value=0.0,
                step=0.1
            )

            nueva_incertidumbre = st.number_input(
                "Incertidumbre",
                min_value=0.0,
                step=0.1
            )

            nuevo_origen = st.selectbox(
                "Origen de los datos",
                [
                    "Manual de instrucciones",
                    "Base de datos",
                    "Medición propia"
                ]
            )

            nueva_fuente = st.text_input("Fuente")

            guardar = st.form_submit_button("Guardar herramienta")

            if guardar:

                nueva_fila = {
                    "herramienta": nueva_herramienta,
                    "situacion": nueva_situacion,
                    "tipo": nuevo_tipo,
                    "aceleracion": nueva_aceleracion,
                    "incertidumbre": nueva_incertidumbre,
                    "origen": nuevo_origen,
                    "fuente": nueva_fuente
                }

                df_herramientas.loc[len(df_herramientas)] = nueva_fila

                df_herramientas.to_csv(
                    "herramientas.csv",
                    index=False
                )

                st.success("Herramienta guardada correctamente")

                st.rerun()

    st.divider()

    if st.button("Cerrar sesión"):
        st.session_state.clear()
        st.session_state.reset_counter = 0
        st.session_state.etapa = "formulario"
        st.session_state.modo_acceso = None
        st.rerun()

    st.stop()


# =========================
# ETAPA 1: FORMULARIO
# =========================

if st.session_state.etapa == "formulario":

    with st.container(border=True):

        st.markdown("### Paso 1 · Datos de exposición")

        st.markdown(
            '<p class="compact-text">Evalúa la exposición a vibraciones mano-brazo según el tiempo de uso y la aceleración estimada de las herramientas.</p>',
            unsafe_allow_html=True
        )

        st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)

        tipo_vibracion = "Mano-brazo"

        LIMITE = 100
        VLE = 400

        col_info1, col_info2, col_info3 = st.columns(3)

        with col_info1:
            mostrar_dato("Tipo de vibración", "Mano-brazo")

        with col_info2:
            mostrar_dato("Nivel de acción", "100 puntos", "metric-action")

        with col_info3:
            mostrar_dato("Valor límite", "400 puntos", "metric-limit")

    st.divider()

    df_filtrado = df_herramientas[df_herramientas["tipo"] == tipo_vibracion]

    if df_filtrado.empty:
        st.error("No hay herramientas registradas para este tipo de vibración en herramientas.csv.")
        st.stop()

    with st.container(border=True):

        st.markdown("### Paso 2 · Herramientas utilizadas")

        num_tareas = st.number_input(
            "¿Cuántas herramientas o equipos vas a utilizar?",
            min_value=1,
            step=1,
            key=f"num_tareas_{st.session_state.reset_counter}"
        )

    tareas = []

    for i in range(num_tareas):

        with st.container(border=True):

            st.markdown(f"#### Operación {i + 1}")

            herramientas_disponibles = df_filtrado["herramienta"].unique().tolist()

            col1, col2 = st.columns(2)

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
            fuente = str(datos_herramienta["fuente"])

            aceleracion_usada = aceleracion + incertidumbre

            tiempo = st.number_input(
                f"Tiempo de uso operación {i + 1} (horas)",
                min_value=0.0,
                step=0.1,
                key=f"tiempo_{i}_{st.session_state.reset_counter}"
            )

            k = 1
            eje = "-"

            tareas.append({
                "nombre": herramienta,
                "situacion": situacion,
                "a_declarada": aceleracion,
                "incertidumbre": incertidumbre,
                "a": aceleracion_usada,
                "fuente": fuente,
                "t": tiempo,
                "tipo": tipo_vibracion,
                "eje": eje,
                "k": k
            })

    st.divider()

    if st.button("SIGUIENTE → CALCULAR EXPOSICIÓN"):
        st.session_state["tareas_calculadas"] = tareas
        st.session_state["tipo_calculado"] = tipo_vibracion
        st.session_state["limite_calculado"] = LIMITE
        st.session_state["vle_calculado"] = VLE
        st.session_state.etapa = "resultado"
        st.rerun()



# =========================
# ETAPA 2: RESULTADO INICIAL
# =========================

elif st.session_state.etapa == "resultado":

    tareas = st.session_state["tareas_calculadas"]
    tipo_vibracion = st.session_state["tipo_calculado"]
    LIMITE = st.session_state["limite_calculado"]
    VLE = st.session_state["vle_calculado"]

    with st.container(border=True):

        st.markdown("### Paso 3 · Resultado inicial")

        puntos_totales = 0

        filas_tabla = [[
            "Herramienta/equipo",
            "Situación",
            "Tipo",
            "Eje",
            "ah declarado",
            "K",
            "ah usado",
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
                str(tarea["a"]),
                str(tarea["t"]),
                str(round(puntos, 2))
            ])

            filas_resumen.append({
                "Herramienta": tarea["nombre"],
                "Situación": tarea["situacion"],
                "Tiempo (h)": tarea["t"],
                "ah usado (m/s²)": tarea["a"],
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
            st.error("Resultado inicial: se supera el valor límite de exposición.")
            estado = "Se supera el valor límite de exposición (VLE)."
        elif puntos_totales >= LIMITE:
            st.warning("Resultado inicial: se supera el nivel de acción.")
            estado = "Se supera el nivel de acción."
        else:
            st.success("Resultado inicial: nivel seguro.")
            estado = "Nivel seguro."

        st.session_state["estado"] = estado

    st.divider()

    with st.container(border=True):

        st.markdown("### Desglose por herramienta")

        df_resumen = pd.DataFrame(filas_resumen)

        st.dataframe(
            df_resumen,
            use_container_width=True,
            hide_index=True,
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

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← ANTERIOR"):
            st.session_state.etapa = "formulario"
            st.rerun()

    with col2:
        if st.button("AJUSTAR EXPOSICIÓN →"):
            st.session_state.etapa = "ajuste"
            st.rerun()


# =========================
# ETAPA 3: AJUSTE DE EXPOSICIÓN
# =========================

elif st.session_state.etapa == "ajuste":

    tareas = st.session_state["tareas_calculadas"]
    tipo_vibracion = st.session_state["tipo_calculado"]
    LIMITE = st.session_state["limite_calculado"]
    VLE = st.session_state["vle_calculado"]
    puntos_totales = st.session_state["puntos_totales"]

    with st.container(border=True):

        st.markdown("### Paso 4 · Ajuste de exposición")

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

    if tipo_ajuste == "Modificar exposición total":

        with st.container(border=True):

            st.markdown("### Ajuste por exposición total")

            st.markdown("""
            Selecciona el objetivo de puntos totales.  
            La reducción se aplicará proporcionalmente según el peso de cada herramienta en el total.
            """)

            objetivo = st.slider(
                "Objetivo de puntos totales",
                min_value=0,
                max_value=max(int(round(puntos_totales)), 1),
                value=min(LIMITE, max(int(round(puntos_totales)), 1)),
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

            col1, col2 = st.columns(2)

            with col1:
                if st.button("← ANTERIOR"):
                    st.session_state.etapa = "resultado"
                    st.rerun()

            with col2:
                if st.button("APLICAR AJUSTE →"):

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

                objetivo_herramienta = st.slider(
                    f"{tarea['nombre']} · {tarea['situacion']}",
                    min_value=0,
                    max_value=max(int(round(puntos_actuales * 1.5)), 1),
                    value=int(round(puntos_actuales)),
                    step=1,
                    key=f"slider_individual_{i}"
                )

                if puntos_actuales > 0:
                    nuevo_tiempo = tarea["t"] * (objetivo_herramienta / puntos_actuales)
                else:
                    nuevo_tiempo = 0

                nueva_tarea = tarea.copy()
                nueva_tarea["t_original"] = tarea["t"]
                nueva_tarea["puntos_originales"] = puntos_actuales
                nueva_tarea["t"] = round(nuevo_tiempo, 2)
                nueva_tarea["puntos_ajustados"] = calcular_puntos(nueva_tarea)

                nuevo_total_individual += nueva_tarea["puntos_ajustados"]
                tareas_individuales.append(nueva_tarea)

                pasos_individuales.append(
                    f"{tarea['nombre']} ({tarea['situacion']}): "
                    f"{round(puntos_actuales, 2)} puntos → "
                    f"{round(nueva_tarea['puntos_ajustados'], 2)} puntos | "
                    f"{tarea['t']} h → {nueva_tarea['t']} h"
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
                st.error("Con estos ajustes se supera el VLE.")
            elif nuevo_total_individual >= LIMITE:
                st.warning("Con estos ajustes se supera el nivel de acción.")
            else:
                st.success("Con estos ajustes no se supera el nivel de acción.")

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
                    "Tiempo ajustado (h)": tarea["t"],
                    "Diferencia (h)": round(diferencia_tiempo, 2)
                })

            df_individual = pd.DataFrame(filas_individuales)

            st.dataframe(
                df_individual,
                use_container_width=True,
                hide_index=True,
                height=min(260, 80 + 35 * len(df_individual))
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("← ANTERIOR"):
                st.session_state.etapa = "resultado"
                st.rerun()

        with col2:
            if st.button("APLICAR AJUSTE INDIVIDUAL →"):

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

        st.markdown("### Paso 5 · Resultado ajustado")

        col_a1, col_a2, col_a3 = st.columns(3)

        with col_a1:
            mostrar_dato("Objetivo seleccionado", objetivo)

        with col_a2:
            mostrar_dato("Total inicial", round(puntos_totales, 2), "metric-action")

        with col_a3:
            mostrar_dato("Total ajustado", round(nuevo_total, 2))

        if nuevo_total >= VLE:
            st.error("Con el ajuste seleccionado se supera el VLE.")
        elif nuevo_total >= LIMITE:
            st.warning("Con el ajuste seleccionado se supera el nivel de acción.")
        else:
            st.success("Con el ajuste seleccionado no se supera el nivel de acción.")

    st.divider()

    with st.container(border=True):

        st.markdown("### Nuevos tiempos propuestos")

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
                "Tiempo ajustado (h)": tarea["t"],
                "Puntos ajustados": round(puntos_ajustados, 2)
            })

            filas_tabla_ajustada.append([
                tarea["nombre"],
                tarea["situacion"],
                str(tarea["t_original"]),
                str(tarea["t"]),
                str(round(puntos_ajustados, 2))
            ])

        df_ajustado = pd.DataFrame(filas_ajustadas_resumen)

        st.dataframe(
            df_ajustado,
            use_container_width=True,
            hide_index=True,
            height=min(240, 80 + 35 * len(df_ajustado))
        )

    st.divider()

    with st.expander("Ver proceso de reducción aplicado"):

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
            str(tarea["t"]),
            str(round(puntos_iniciales, 2)),
            str(round(puntos_ajustados, 2))
        ])

    pdf = generar_pdf(
        "Resultado de evaluación",
        resumen_pdf,
        filas_pdf,
        conclusion_pdf
    )

    with open(pdf, "rb") as file:
        st.download_button(
            label="📄 DESCARGAR INFORME EN PDF",
            data=file,
            file_name="informe_vibraciones.pdf",
            mime="application/pdf"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← ANTERIOR"):
            st.session_state.etapa = "ajuste"
            st.rerun()

    with col2:
        if st.button("NUEVA EVALUACIÓN"):
            st.session_state.clear()
            st.session_state.reset_counter = 0
            st.session_state.etapa = "formulario"
            st.session_state.modo_acceso = None
            st.rerun()


