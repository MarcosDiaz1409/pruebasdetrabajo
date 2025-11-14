import streamlit as st
from fpdf import FPDF  # <- NUEVO
from io import BytesIO  # <- NUEVO

# ----------------- CONFIGURACIÓN BÁSICA -----------------
st.set_page_config(
    page_title="Ficha de Proyectos",
    page_icon="📋",
    layout="wide"
)

# Estilos simples para que se vea más agradable
st.markdown(
    """
    <style>
    .main > div {
        padding-top: 1rem;
    }
    .card {
        background-color: #ffffff;
        padding: 1.5rem 1.75rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.12);
        margin-bottom: 1.5rem;
        border: 1px solid #e5e7eb;
    }
    .tag {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        font-size: 0.75rem;
        background-color: #eef2ff;
        color: #3730a3;
        margin-right: 0.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- ESTADO INICIAL -----------------
if "proyectos" not in st.session_state:
    st.session_state["proyectos"] = []  # lista de dicts


# ----------------- FUNCIÓN PARA CREAR PDF -----------------
def crear_pdf_proyecto(proyecto: dict) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Encabezado
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Ficha de Proyecto", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", "", 11)

    # Helper para escribir título + valor
    def linea(titulo, valor=""):
        texto = f"{titulo}: {valor}"
        pdf.multi_cell(0, 6, texto)

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
    pdf.multi_cell(0, 6, proyecto.get("resumen_auto", ""))
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "Descripción", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, proyecto.get("descripcion", ""))
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "Observaciones internas", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, proyecto.get("observaciones", ""))

    # Devolver como bytes
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return pdf_bytes


# ----------------- TÍTULO -----------------
st.title("📋 Ficha de Registro de Proyectos")
st.caption(
    "Formulario para capturar información básica de proyectos y generar campos derivados "
    "automáticamente para estandarizar la información."
)

# ----------------- FORMULARIO PRINCIPAL -----------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Datos de la ficha")

    with st.form("ficha_proyecto", clear_on_submit=False):

        # ---------- DATOS GENERALES ----------
        st.markdown("### 1. Datos generales")

        col1, col2, col3 = st.columns(3)

        with col1:
            codigo_proyecto = st.text_input(
                "Código de proyecto*",
                placeholder="Ej. 2025-001"
            )
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
            nivel_prioridad = st.selectbox(
                "Nivel de prioridad",
                options=["Alta", "Media", "Baja"],
                index=0
            )

        with col2:
            nombre_propuesto = st.text_input(
                "Nombre propuesto del proyecto*",
                placeholder="Ej. Mejoramiento de camino rural..."
            )
            objetivo = st.selectbox(
                "Objetivo estratégico*",
                options=[
                    "Objetivo 10",
                    "Objetivo 20",
                    "Objetivo 30",
                    "Objetivo 40"
                ],
                index=2  # por defecto "Objetivo 30"
            )
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

        with col3:
            anio = st.number_input(
                "Año de inicio*",
                min_value=2000,
                max_value=2100,
                value=2025,
                step=1
            )
            tipo_proyecto = st.selectbox(
                "Tipo de proyecto",
                options=["Nuevo", "Continuidad", "Ampliación de alcance"],
                index=0
            )
            estado = st.selectbox(
                "Estado de la ficha",
                options=["Borrador", "En revisión", "Aprobado"],
                index=0
            )

        # ---------- LOCALIZACIÓN ----------
        st.markdown("### 2. Localización")

        col_loc1, col_loc2, col_loc3 = st.columns(3)

        with col_loc1:
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

        with col_loc2:
            municipio = st.text_input(
                "Municipio*",
                placeholder="Ej. Cobán"
            )

        with col_loc3:
            zona = st.text_input(
                "Comunidad / localidad",
                placeholder="Opcional"
            )

        # ---------- CLASIFICACIÓN Y RESPONSABLES ----------
        st.markdown("### 3. Clasificación y responsables")

        col_clas1, col_clas2, col_clas3 = st.columns(3)

        with col_clas1:
            unidad_ejecutora = st.text_input(
                "Unidad ejecutora*",
                placeholder="Ej. Dirección de Caminos"
            )
        with col_clas2:
            programa = st.text_input(
                "Programa presupuestario",
                placeholder="Ej. 12 - Infraestructura vial"
            )
        with col_clas3:
            fuente_financiamiento = st.selectbox(
                "Fuente de financiamiento",
                options=[
                    "Recursos nacionales",
                    "Préstamo externo",
                    "Donación",
                    "Mixto"
                ]
            )

        # ---------- MONTOS ----------
        st.markdown("### 4. Montos estimados (Q)")

        col_monto1, col_monto2, col_monto3 = st.columns(3)

        with col_monto1:
            monto_estimado = st.number_input(
                "Monto total estimado*",
                min_value=0.0,
                value=0.0,
                step=50000.0,
                format="%.2f"
            )
        with col_monto2:
            contrapartida_local = st.number_input(
                "Contrapartida local",
                min_value=0.0,
                value=0.0,
                step=10000.0,
                format="%.2f"
            )
        with col_monto3:
            duracion_meses = st.number_input(
                "Duración estimada (meses)",
                min_value=1,
                max_value=120,
                value=12,
                step=1
            )

        # ---------- CAMPOS DERIVADOS (SOLO LECTURA) ----------
        st.markdown("### 5. Campos calculados (solo lectura)")


        def safe(v, alt=""):
            return v if v not in (None, "", 0) else alt


        # 1) Título automático = "Proceso Objetivo 30"
        titulo_automatico = ""
        if safe(proceso) and safe(objetivo):
            titulo_automatico = f"{proceso} {objetivo}"

        # 2) Código completo = ANIO-DEP-CODIGO
        depto_abrev = safe(departamento, "SINDEP")[:3].upper() if departamento else "SINDEP"
        codigo_completo = ""
        if safe(codigo_proyecto):
            codigo_completo = f"{anio}-{depto_abrev}-{codigo_proyecto}"

        # 3) Etiqueta para reportes = "Tipo - Eje - Prioridad"
        etiqueta_reporte = f"{tipo_proyecto} | {eje_estrategico} | {nivel_prioridad}"

        # 4) Resumen automático corto
        resumen_auto = (
            f"Proyecto orientado al {objetivo} bajo el proceso de {proceso}, "
            f"ubicado en {safe(municipio, 'municipio por definir')}, {safe(departamento, 'departamento por definir')}. "
            f"Monto estimado: Q{monto_estimado:,.2f} en aproximadamente {duracion_meses} meses."
        )

        col_calc1, col_calc2 = st.columns(2)

        with col_calc1:
            st.text_input(
                "Título automático",
                value=titulo_automatico,
                disabled=True
            )
            st.text_input(
                "Código completo para sistema",
                value=codigo_completo,
                disabled=True
            )

        with col_calc2:
            st.text_input(
                "Etiqueta para reportes",
                value=etiqueta_reporte,
                disabled=True
            )
            st.text_area(
                "Resumen automático",
                value=resumen_auto,
                disabled=True,
                height=100
            )

        # ---------- DESCRIPCIÓN LIBRE ----------
        st.markdown("### 6. Descripción y observaciones")

        descripcion = st.text_area(
            "Descripción breve del proyecto",
            placeholder="Describe el problema que atiende, el público objetivo y el resultado esperado...",
            height=120
        )

        observaciones = st.text_area(
            "Observaciones internas",
            placeholder="Notas internas, supuestos, riesgos, etc.",
            height=100
        )

        # ---------- BOTÓN DE ENVÍO ----------
        submitted = st.form_submit_button("💾 Guardar ficha")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- VALIDACIÓN Y GUARDADO -----------------
if submitted:
    errores = []

    # Validar campos obligatorios
    if not codigo_proyecto.strip():
        errores.append("El campo **Código de proyecto** es obligatorio.")
    if not nombre_propuesto.strip():
        errores.append("El campo **Nombre propuesto del proyecto** es obligatorio.")
    if not departamento:
        errores.append("Debe seleccionar un **Departamento**.")
    if not municipio.strip():
        errores.append("El campo **Municipio** es obligatorio.")
    if not unidad_ejecutora.strip():
        errores.append("El campo **Unidad ejecutora** es obligatorio.")
    if monto_estimado <= 0:
        errores.append("El **Monto total estimado** debe ser mayor que 0.")

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
            # Campos derivados
            "titulo_automatico": titulo_automatico,
            "codigo_completo": codigo_completo,
            "etiqueta_reporte": etiqueta_reporte,
            "resumen_auto": resumen_auto,
            # Campos texto libre
            "descripcion": descripcion,
            "observaciones": observaciones,
        }

        st.session_state["proyectos"].append(proyecto)
        st.success(
            "✅ Ficha guardada correctamente. Puedes seguir capturando o revisar el listado de proyectos más abajo.")

# ----------------- LISTADO DE PROYECTOS Y PDF -----------------
if st.session_state["proyectos"]:
    st.markdown("## 🗂 Proyectos capturados en esta sesión")

    # Vista tipo tarjeta del último proyecto
    ultimo = st.session_state["proyectos"][-1]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"**Último proyecto registrado:** `{ultimo['codigo_completo']}`")
    st.markdown(
        f"<span class='tag'>{ultimo['estado']}</span>"
        f"<span class='tag'>{ultimo['nivel_prioridad']}</span>"
        f"<span class='tag'>{ultimo['eje_estrategico']}</span>",
        unsafe_allow_html=True
    )

    st.markdown(f"### {ultimo['titulo_automatico']}")
    st.markdown(f"**Nombre propuesto:** {ultimo['nombre_propuesto']}")
    st.markdown(
        f"**Ubicación:** {ultimo['municipio']}, {ultimo['departamento']} "
        f"• **Unidad ejecutora:** {ultimo['unidad_ejecutora']}"
    )
    st.markdown(
        f"**Monto estimado:** Q{ultimo['monto_estimado']:,.2f} "
        f"({ultimo['fuente_financiamiento']})"
    )
    st.markdown(f"**Resumen automático:** {ultimo['resumen_auto']}")

    # --------- NUEVO: APARTADO PARA PDF ---------
    st.markdown("### 📄 Exportar resumen en PDF")

    pdf_bytes = crear_pdf_proyecto(ultimo)

    st.download_button(
        label="⬇️ Descargar PDF del último proyecto",
        data=pdf_bytes,
        file_name=f"ficha_{ultimo['codigo_completo'] or 'proyecto'}.pdf",
        mime="application/pdf"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Tabla con todos los proyectos
    st.markdown("### Tabla de proyectos capturados")
    st.dataframe(st.session_state["proyectos"], use_container_width=True)
