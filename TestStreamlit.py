import streamlit as st
from fpdf import FPDF

# ================== CONFIGURACIÓN GLOBAL ==================
st.set_page_config(
    page_title="Registro de Proyectos",
    layout="wide"
)

# Ocultar menús, badges y elementos de Streamlit
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}

        .viewerBadge_container__1QSob,
        .viewerBadge_link__1S137,
        .viewerBadge_text__1JaDK,
        .styles_viewerBadge__1yB5_,
        .styles_viewerBadge,
        .stStatusWidget,
        .stAppToolbar,
        .stToolbar,
        .stDecoration,
        .st-emotion-cache-16huue1,
        .st-emotion-cache-1gwvy71 {
            display: none !important;
            visibility: hidden !important;
        }

        div[data-testid="stStatusWidget"],
        div[data-testid="stDecoration"] {
            display: none !important;
            visibility: hidden !important;
        }

        div[style*="position: fixed"][style*="bottom: 0px"][style*="right: 0px"] {
            display: none !important;
            visibility: hidden !important;
        }

        a[href*="streamlit.io"] {
            display: none !important;
            visibility: hidden !important;
        }

        div[aria-label*="Created"],
        div[aria-label*="Hosted"],
        div[aria-label*="Streamlit"] {
            display: none !important;
            visibility: hidden !important;
        }

        .stApp {
            background-color: #f3f4f6;
        }

        .main > div {
            padding-top: 0.5rem;
        }

        .app-header {
            padding: 1.25rem 1.5rem 0.75rem 1.5rem;
            background-color: #ffffff;
            border-bottom: 1px solid #e5e7eb;
            margin-bottom: 1rem;
        }

        .app-title {
            font-size: 1.6rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.1rem;
        }

        .app-subtitle {
            font-size: 0.9rem;
            color: #6b7280;
        }

        .card {
            background-color: #ffffff;
            padding: 1.2rem 1.4rem;
            border-radius: 0.9rem;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
            margin-bottom: 1.2rem;
            border: 1px solid #e5e7eb;
        }

        .card-header {
            font-size: 1.0rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.6rem;
        }

        .tag {
            display: inline-block;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            background-color: #eef2ff;
            color: #3730a3;
            margin-right: 0.25rem;
            margin-top: 0.3rem;
        }

        .kpi-card {
            background-color: #ffffff;
            padding: 0.9rem 1.0rem;
            border-radius: 0.9rem;
            border: 1px solid #e5e7eb;
        }

        .kpi-label {
            font-size: 0.75rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.2rem;
        }

        .kpi-value {
            font-size: 1.2rem;
            font-weight: 600;
            color: #111827;
        }

        .kpi-subvalue {
            font-size: 0.8rem;
            color: #6b7280;
            margin-top: 0.1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== ESTADO ==================
if "proyectos" not in st.session_state:
    st.session_state["proyectos"] = []


def crear_pdf_proyecto(proyecto: dict) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Márgenes explícitos
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)

    pdf.add_page()

    # Encabezado
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Ficha de Proyecto", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", "", 11)

    # Ancho útil de la página (ya descontando márgenes)
    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    def linea(titulo, valor=""):
        # Asegurarse de que siempre sea texto
        texto = f"{titulo}: {valor}"
        texto = str(texto)
        # Usar un ancho fijo (page_width) en lugar de 0
        pdf.multi_cell(page_width, 6, texto)

    linea("Código completo", proyecto.get("codigo_completo", ""))
    linea("Título automático", proyecto.get("titulo_automatico", ""))
    linea("Nombre propuesto", proyecto.get("nombre_propuesto", ""))
    pdf.ln(3)

    linea("Proceso", proyecto.get("proceso", ""))
    linea("Objetivo estratégico", proyecto.get("objetivo", ""))
    linea("Tipo de proyecto", proyecto.get("tipo_proyecto", ""))
    linea("Eje estratégico", proyecto.get("eje_estrategico", ""))
    linea("Nivel de prioridad", proyecto.get("nivel_prioridad", ""))
    linea("Estado de la ficha", proyecto.get("estado", ""))
    pdf.ln(3)

    linea(
        "Ubicación",
        f"{proyecto.get('municipio', '')}, {proyecto.get('departamento', '')}"
    )
    linea("Unidad ejecutora", proyecto.get("unidad_ejecutora", ""))
    linea("Programa presupuestario", proyecto.get("programa", ""))
    linea("Fuente de financiamiento", proyecto.get("fuente_financiamiento", ""))
    pdf.ln(3)

    linea(
        "Monto estimado",
        f"Q{proyecto.get('monto_estimado', 0):,.2f}"
    )
    linea(
        "Contrapartida local",
        f"Q{proyecto.get('contrapartida_local', 0):,.2f}"
    )
    linea(
        "Duración estimada (meses)",
        proyecto.get("duracion_meses", "")
    )
    pdf.ln(4)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "Resumen automático", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(page_width, 6, str(proyecto.get("resumen_auto", "")))
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "Descripción", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(page_width, 6, str(proyecto.get("descripcion", "")))
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "Observaciones internas", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(page_width, 6, str(proyecto.get("observaciones", "")))

    # Compatibilidad con distintas versiones de fpdf/fpdf2
    result = pdf.output(dest="S")

    # En algunas versiones devuelve str, en otras bytes/bytearray
    if isinstance(result, str):
        pdf_bytes = result.encode("latin-1")
    else:
        pdf_bytes = bytes(result)

    return pdf_bytes



# ================== ENCABEZADO ==================
st.markdown(
    """
    <div class="app-header">
        <div class="app-title">Panel de registro y seguimiento de proyectos</div>
        <div class="app-subtitle">
            Plataforma para configurar proyectos, visualizar en tiempo real los campos derivados
            y consolidar un registro estándar para análisis y monitoreo.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ================== LAYOUT TIPO DASHBOARD ==================
col_config, col_preview, col_resumen = st.columns([1.3, 1.7, 1.4])

# =====================================================================
#                     COLUMNA 1: CONFIGURACIÓN / CAPTURA
# =====================================================================
with col_config:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Configuración del proyecto</div>', unsafe_allow_html=True)

    st.caption("Complete los campos para configurar el proyecto actual.")

    # Bloque de identificación
    st.markdown("**Identificación básica**")
    codigo_proyecto = st.text_input(
        "Código de proyecto*",
        placeholder="Ej. 2025-001"
    )
    nombre_propuesto = st.text_input(
        "Nombre propuesto del proyecto*",
        placeholder="Ej. Mejoramiento de camino rural..."
    )

    col1a, col1b = st.columns(2)
    with col1a:
        proceso = st.selectbox(
            "Proceso*",
            options=[
                "Mejoramiento",
                "Construcción",
                "Ampliación",
                "Rehabilitación",
                "Mantenimiento"
            ],
            index=0
        )
        tipo_proyecto = st.selectbox(
            "Tipo de proyecto",
            options=["Nuevo", "Continuidad", "Ampliación de alcance"],
            index=0
        )
    with col1b:
        objetivo = st.selectbox(
            "Objetivo estratégico*",
            options=[
                "Objetivo 10",
                "Objetivo 20",
                "Objetivo 30",
                "Objetivo 40"
            ],
            index=2
        )
        anio = st.number_input(
            "Año de inicio*",
            min_value=2000,
            max_value=2100,
            value=2025,
            step=1
        )

    st.markdown("---")

    # Localización
    st.markdown("**Localización y enfoque**")
    departamento = st.selectbox(
        "Departamento*",
        options=[
            "",
            "Guatemala",
            "Huehuetenango",
            "Alta Verapaz",
            "Quiché",
            "Petén",
            "Chimaltenango",
            "Escuintla",
            "San Marcos"
        ],
        index=1
    )
    municipio = st.text_input(
        "Municipio*",
        placeholder="Ej. Cobán"
    )
    zona = st.text_input(
        "Comunidad / localidad",
        placeholder="Opcional"
    )

    col2a, col2b = st.columns(2)
    with col2a:
        eje_estrategico = st.selectbox(
            "Eje estratégico",
            options=[
                "Infraestructura",
                "Desarrollo social",
                "Desarrollo económico",
                "Gestión ambiental",
                "Gobernanza"
            ]
        )
        nivel_prioridad = st.selectbox(
            "Nivel de prioridad",
            options=["Alta", "Media", "Baja"],
            index=0
        )
    with col2b:
        estado = st.selectbox(
            "Estado de la ficha",
            options=["Borrador", "En revisión", "Aprobado"],
            index=0
        )

    st.markdown("---")

    # Clasificación institucional
    st.markdown("**Clasificación institucional**")
    unidad_ejecutora = st.text_input(
        "Unidad ejecutora*",
        placeholder="Ej. Dirección de Caminos"
    )
    col3a, col3b = st.columns(2)
    with col3a:
        programa = st.text_input(
            "Programa presupuestario",
            placeholder="Ej. 12 - Infraestructura vial"
        )
    with col3b:
        fuente_financiamiento = st.selectbox(
            "Fuente de financiamiento",
            options=[
                "Recursos nacionales",
                "Préstamo externo",
                "Donación",
                "Mixto"
            ]
        )

    st.markdown("---")

    # Montos
    st.markdown("**Montos y horizonte**")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        monto_estimado = st.number_input(
            "Monto total estimado*",
            min_value=0.0,
            value=0.0,
            step=50000.0,
            format="%.2f"
        )
    with col_m2:
        contrapartida_local = st.number_input(
            "Contrapartida local",
            min_value=0.0,
            value=0.0,
            step=10000.0,
            format="%.2f"
        )
    with col_m3:
        duracion_meses = st.number_input(
            "Duración estimada (meses)",
            min_value=1,
            max_value=120,
            value=12,
            step=1
        )

    st.markdown("---")

    # Descripción
    st.markdown("**Descripción y observaciones**")
    descripcion = st.text_area(
        "Descripción breve del proyecto",
        placeholder="Describa el problema que atiende, el público objetivo y el resultado esperado...",
        height=110
    )
    observaciones = st.text_area(
        "Observaciones internas",
        placeholder="Notas internas, supuestos, riesgos, etc.",
        height=90
    )

    st.markdown("---")

    # Botón de guardado
    guardar = st.button("Guardar proyecto en el registro")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================
#                  CAMPOS DERIVADOS Y VALIDACIÓN (COMPARTIDO)
# =====================================================================
def safe(v, alt=""):
    return v if v not in (None, "", 0) else alt

# Campos derivados
titulo_automatico = ""
if safe(proceso) and safe(objetivo):
    titulo_automatico = f"{proceso} {objetivo}"

depto_abrev = safe(departamento, "SINDEP")[:3].upper() if departamento else "SINDEP"
codigo_completo = ""
if safe(codigo_proyecto):
    codigo_completo = f"{anio}-{depto_abrev}-{codigo_proyecto}"

etiqueta_reporte = f"{tipo_proyecto} | {eje_estrategico} | {nivel_prioridad}"

resumen_auto = (
    f"Proyecto orientado al {objetivo} bajo el proceso de {proceso}, "
    f"ubicado en {safe(municipio, 'municipio por definir')}, {safe(departamento, 'departamento por definir')}. "
    f"Monto estimado: Q{monto_estimado:,.2f} en aproximadamente {duracion_meses} meses."
)

# =====================================================================
#                  GUARDADO EN SESIÓN CUANDO SE PRESIONA EL BOTÓN
# =====================================================================
if guardar:
    errores = []

    if not codigo_proyecto.strip():
        errores.append("El campo Código de proyecto es obligatorio.")
    if not nombre_propuesto.strip():
        errores.append("El campo Nombre propuesto del proyecto es obligatorio.")
    if not departamento:
        errores.append("Debe seleccionar un Departamento.")
    if not municipio.strip():
        errores.append("El campo Municipio es obligatorio.")
    if not unidad_ejecutora.strip():
        errores.append("El campo Unidad ejecutora es obligatorio.")
    if monto_estimado <= 0:
        errores.append("El Monto total estimado debe ser mayor que 0.")

    if errores:
        for e in errores:
            st.error(e)
    else:
        proyecto = {
            "codigo_proyecto": codigo_proyecto,
            "nombre_propuesto": nombre_propuesto,
            "proceso": proceso,
            "objetivo": objetivo,
            "anio": int(anio),
            "departamento": departamento,
            "municipio": municipio,
            "zona": zona,
            "unidad_ejecutora": unidad_ejecutora,
            "programa": programa,
            "fuente_financiamiento": fuente_financiamiento,
            "monto_estimado": float(monto_estimado),
            "contrapartida_local": float(contrapartida_local),
            "duracion_meses": int(duracion_meses),
            "nivel_prioridad": nivel_prioridad,
            "tipo_proyecto": tipo_proyecto,
            "eje_estrategico": eje_estrategico,
            "estado": estado,
            "titulo_automatico": titulo_automatico,
            "codigo_completo": codigo_completo,
            "etiqueta_reporte": etiqueta_reporte,
            "resumen_auto": resumen_auto,
            "descripcion": descripcion,
            "observaciones": observaciones,
        }

        st.session_state["proyectos"].append(proyecto)
        st.success("Proyecto guardado en el registro de la sesión.")

# =====================================================================
#                     COLUMNA 2: VISTA PREVIA DINÁMICA
# =====================================================================
with col_preview:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Vista previa del proyecto en diseño</div>', unsafe_allow_html=True)

    st.caption("Se muestran los campos derivados y un resumen del proyecto con base en la configuración actual.")

    st.markdown(f"**Título automático:** {titulo_automatico or 'Pendiente de completar información'}")
    st.markdown(f"**Código completo propuesto:** `{codigo_completo or 'Pendiente'}`")
    st.markdown(f"**Etiqueta para reportes:** {etiqueta_reporte}")

    st.markdown("---")
    st.markdown("**Resumen automático:**")
    st.write(resumen_auto)

    st.markdown("---")
    st.markdown("**Ubicación y enfoque:**")
    st.write(
        f"- Departamento: {departamento or 'Sin definir'}\n"
        f"- Municipio: {municipio or 'Sin definir'}\n"
        f"- Comunidad / localidad: {zona or 'Sin especificar'}\n"
        f"- Eje estratégico: {eje_estrategico}\n"
        f"- Nivel de prioridad: {nivel_prioridad}\n"
        f"- Estado de la ficha: {estado}"
    )

    st.markdown("---")
    st.markdown("**Montos y horizonte estimado:**")
    st.write(
        f"- Monto total estimado: Q{monto_estimado:,.2f}\n"
        f"- Contrapartida local: Q{contrapartida_local:,.2f}\n"
        f"- Duración estimada: {duracion_meses} meses"
    )

    st.markdown("---")
    st.markdown("**Descripción propuesta:**")
    st.write(descripcion or "Sin descripción registrada.")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================
#                     COLUMNA 3: RESUMEN Y PDF
# =====================================================================
with col_resumen:
    proyectos = st.session_state["proyectos"]

    # KPIs
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Indicadores de la sesión</div>', unsafe_allow_html=True)

    colk1, colk2 = st.columns(2)
    with colk1:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Proyectos registrados</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-value">{len(proyectos)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with colk2:
        total_monto = sum(p.get("monto_estimado", 0) for p in proyectos) if proyectos else 0
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Monto total estimado</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-value">Q{total_monto:,.2f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Detalle último proyecto y PDF
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Último proyecto registrado</div>', unsafe_allow_html=True)

    if proyectos:
        ultimo = proyectos[-1]

        st.markdown(f"**Código completo:** `{ultimo.get('codigo_completo', '')}`")
        st.markdown(
            f"<span class='tag'>{ultimo.get('estado', '')}</span>"
            f"<span class='tag'>{ultimo.get('nivel_prioridad', '')}</span>"
            f"<span class='tag'>{ultimo.get('eje_estrategico', '')}</span>",
            unsafe_allow_html=True
        )

        st.markdown(f"**Título automático:** {ultimo.get('titulo_automatico', '')}")
        st.markdown(f"**Nombre propuesto:** {ultimo.get('nombre_propuesto', '')}")
        st.markdown(
            f"**Ubicación:** {ultimo.get('municipio', '')}, {ultimo.get('departamento', '')}"
        )
        st.markdown(
            f"**Monto estimado:** Q{ultimo.get('monto_estimado', 0):,.2f} "
            f"({ultimo.get('fuente_financiamiento', '')})"
        )

        st.markdown("---")
        st.markdown("Resumen automático del proyecto:")
        st.write(ultimo.get("resumen_auto", ""))

        st.markdown("---")
        pdf_bytes = crear_pdf_proyecto(ultimo)
        st.download_button(
            label="Descargar PDF del último proyecto",
            data=pdf_bytes,
            file_name=f"ficha_{ultimo.get('codigo_completo') or 'proyecto'}.pdf",
            mime="application/pdf"
        )
    else:
        st.info("Aún no hay proyectos registrados en la sesión.")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================
#                 TABLA GENERAL DE PROYECTOS (PARTE INFERIOR)
# =====================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">Registro de proyectos de la sesión</div>', unsafe_allow_html=True)

if st.session_state["proyectos"]:
    st.dataframe(st.session_state["proyectos"], use_container_width=True)
else:
    st.info("El registro aún no contiene proyectos. Configure uno en el panel izquierdo y guárdelo.")

st.markdown('</div>', unsafe_allow_html=True)
