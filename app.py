import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DEL SISTEMA Y BLINDAJE CONTRA INTERFERENCIAS DE NAVEGADOR
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NEURO-CLUSTER B | Plataforma Computacional de Fenotipado Dimensional",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Blindaje contra traductores automáticos para evitar errores de renderizado en React
st.markdown("""
<head>
    <meta name="google" content="notranslate">
</head>
<style>
    html, body, [class*="css"], .stApp {
        translate: no !important;
    }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        letter-spacing: -0.2px;
    }
    div[data-testid="stMetric"] {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 12px 16px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. PANEL LATERAL: PARÁMETROS BIOLÓGICOS, PSICOPATOLÓGICOS Y PSICOTERAPÉUTICOS
# -----------------------------------------------------------------------------
st.sidebar.title("Perfil Clínico Dimensional")
st.sidebar.caption("Parámetros del modelo híbrido (DSM-5 Sección III / CIE-11 / RDoC):")

st.sidebar.subheader("1. Diátesis Biológica y Trauma Temprano")
ctq_score = st.sidebar.slider(
    "Severidad de Trauma Infantil (CTQ: 25-125)",
    min_value=25, max_value=125, value=78, step=1,
    help="Cuestionario de Trauma Infantil. Modula la reactividad del eje HPA y la sensibilidad amigdalina vía metilación de NR3C1."
)

fa_uncinado = st.sidebar.slider(
    "Integridad del Fascículo Uncinado (DTI - FA)",
    min_value=0.30, max_value=0.55, value=0.38, step=0.01,
    help="Anisotropía fraccional. Representa el ancho de banda estructural del freno inhibitorio frontoamigdalino (Sano: 0.46-0.52; Trastorno severo: <0.39)."
)

st.sidebar.subheader("2. Dimensiones Psicométricas (AMPD / HiTOP)")
labilidad_afectiva = st.sidebar.slider(
    "Labilidad Afectiva e Hiperreactividad (0-100%)",
    min_value=0, max_value=100, value=85, step=1,
    help="Sustrato del circuito amígdala-ínsula anterior ante estímulos de valencia negativa."
)

desinhibicion_motora = st.sidebar.slider(
    "Desinhibición e Impulsividad Conductual (0-100%)",
    min_value=0, max_value=100, value=75, step=1,
    help="Falla de control ejecutivo orbitofrontal-estriatal."
)

antagonismo_rasgo = st.sidebar.slider(
    "Antagonismo vs. Empatía Afectiva (0-100%)",
    min_value=0, max_value=100, value=40, step=1,
    help="Valores altos con baja reactividad autonómica perfilan rasgos de psicopatía primaria; con alta labilidad, inestabilidad límite."
)

st.sidebar.subheader("3. Prueba de Carga Afectiva Dinámica")
estres_interpersonal = st.sidebar.slider(
    "Intensidad del Estresor Relacional (0-100)",
    min_value=0, max_value=100, value=60, step=1,
    help="Simula la magnitud del rechazo, abandono percibido o invalidación vincular en tiempo real."
)

st.sidebar.subheader("4. Intervención Psicoterapéutica Basada en Evidencia")
psicoterapia_activa = st.sidebar.selectbox(
    "Programa Terapéutico Estandarizado",
    options=[
        "Sin psicoterapia estructurada (Fase Aguda)",
        "Terapia Dialéctico Conductual (DBT - Regulación Emocional / Malestar)",
        "Tratamiento Basado en Mentalización (MBT - Estabilidad TPJ / mPFC)",
        "Psicoterapia Focalizada en la Transferencia (TFP - Integración Identitaria)"
    ],
    index=0,
    help="Intervenciones manualizadas validadas mediante ensayos clínicos controlados y neuroimagen funcional pre/post tratamiento."
)

st.sidebar.subheader("5. Parámetros Forenses de Riesgo Inmediato")
plan_letal = st.sidebar.select_slider(
    "Estructuración de Plan Letal Objetivo",
    options=["Nulo / Ausente", "Inestructurado / Disperso", "Estructurado / Con acceso a medios"],
    value="Inestructurado / Disperso"
)
soporte_vincular = st.sidebar.radio(
    "Red de Contención Vincular Externa",
    options=["Presente y continente", "Ausente / Severamente disfuncional"],
    index=0
)

# -----------------------------------------------------------------------------
# 3. MOTOR CUANTITATIVO: CONECTÓMICA, NEUROQUÍMICA Y ALGORITMOS PERICIALES
# -----------------------------------------------------------------------------

# Modulación psicoterapéutica sobre el acoplamiento y la reactividad
if "DBT" in psicoterapia_activa:
    factor_resiliencia_psico = 0.42
    desc_psico = "DBT activa: Entrenamiento conductual en regulación y tolerancia al malestar. Atenúa la hiperreactividad amigdalina bilateral e incrementa el reclutamiento de vlPFC (Schmitt et al., 2016)."
elif "MBT" in psicoterapia_activa:
    factor_resiliencia_psico = 0.38
    desc_psico = "MBT activo: Preserva el procesamiento reflexivo en la unión temporoparietal (TPJ) y mPFC, retardando el colapso hacia modalidades pre-mentalizadoras (Bateman & Fonagy, 2016)."
elif "TFP" in psicoterapia_activa:
    factor_resiliencia_psico = 0.35
    desc_psico = "TFP activa: Modula la coherencia de la Red por Defecto (DMN) e integra representaciones disociadas del self y de los otros significativos (Clarkin et al., 2007)."
else:
    factor_resiliencia_psico = 0.0
    desc_psico = "Fase aguda sin abordaje psicoterapéutico: La reactividad límbica opera desprovista de mecanismos compensatorios aprendidos."

# Vulnerabilidad biológica basal modulada por trauma infantil (Eje HPA)
diatesis_trauma = (ctq_score - 25.0) / 100.0  # 0 a 1

# Capacidad basal del freno frontal según integridad de sustancia blanca (DTI)
capacidad_basal_freno = (fa_uncinado - 0.30) / 0.25  # 0 a 1

# Umbral de quiebre homeostático del acoplamiento frontoamigdalino
umbral_quiebre = 45.0 + (capacidad_basal_freno * 25.0) - (diatesis_trauma * 30.0) + (factor_resiliencia_psico * 25.0)

# Ecuación logística de desacoplamiento inhibitorio dlPFC/vlPFC -> Amígdala
sigmoide_estres = 1.0 / (1.0 + np.exp(-(estres_interpersonal - umbral_quiebre) / 7.5))
acoplamiento_frontolimbico = (capacidad_basal_freno * (1.0 - (0.85 * sigmoide_estres)) + (factor_resiliencia_psico * 0.30)) * 100.0
acoplamiento_frontolimbico = float(np.clip(acoplamiento_frontolimbico, 5.0, 98.0))

# Tono basal y dinámico del sistema mu-opioide (MOR en PET [11C]carfentanil)
tono_mor_basal = float(np.clip(100.0 - (labilidad_afectiva * 0.45) - (diatesis_trauma * 35.0), 15.0, 95.0))
angustia_psiquica = float(np.clip((labilidad_afectiva * (estres_interpersonal / 100.0) * 1.3) / (tono_mor_basal / 100.0), 0.0, 100.0))

# Dinámica de Redes Funcionales Mayores (Salience Network vs. Executive Control Network)
actividad_sn = float(np.clip(35.0 + (labilidad_afectiva * 0.40) + (estres_interpersonal * 0.35) - (factor_resiliencia_psico * 20.0), 10.0, 100.0))
actividad_cen = float(np.clip(acoplamiento_frontolimbico * 0.95, 10.0, 100.0))

# Cálculo cuantitativo de riesgo cierto e inminente (Art. 20 Ley 26.657)
pts_plan = 80.0 if "Estructurado" in plan_letal else (35.0 if "Inestructurado" in plan_letal else 0.0)
pts_intencion = float(np.clip((angustia_psiquica * 0.45) + (desinhibicion_motora * 0.40), 10.0, 95.0))
pts_red = 20.0 if "Presente" in soporte_vincular else 85.0

rci_index = (0.40 * pts_plan) + (0.35 * pts_intencion) + (0.25 * pts_red)
rci_index = float(np.clip(rci_index, 5.0, 100.0))

# Clasificación Fenotípica Dimensional (DSM-5 Sección III)
if antagonismo_rasgo >= 70 and labilidad_afectiva < 50:
    fenotipo_ampd = "Patrón Antagónico Primario (Insensible-Emocional)"
    correlato_neuro = "Hiporreactividad amigdalina basal y autonómica, preservación del control ejecutivo prefrontal con desconexión empática ventromedial."
elif labilidad_afectiva >= 70 and desinhibicion_motora >= 65:
    fenotipo_ampd = "Inestabilidad Emocional Severa (Fenotipo Límite Central)"
    correlato_neuro = "Desacoplamiento frontolímbico bifásico, hiperreactividad de ínsula/amígdala y déficit de tono opioide endógeno."
elif antagonismo_rasgo >= 60 and labilidad_afectiva >= 60:
    fenotipo_ampd = "Espectro Mixto Narcisista-Límite (Vulnerabilidad / Grandiosidad Oscilante)"
    correlato_neuro = "Hiperreactividad de la Red de Salienccia ante amenazas al estatus, con fluctuaciones agudas en la Red por Defecto (DMN)."
else:
    fenotipo_ampd = "Organización de Personalidad con Afectación Funcional Moderada"
    correlato_neuro = "Oscilaciones del control inhibitorio circunscritas a picos de estrés relacional agudo sin colapso estructural sostenido."

# -----------------------------------------------------------------------------
# 4. ENCABEZADO Y MÉTRICAS INSTITUCIONALES
# -----------------------------------------------------------------------------
st.title("Plataforma Computacional de Fenotipado Dimensional y Conectómica")
st.markdown("**Modelado Biofísico Corticolímbico, Neuroplasticidad Psicoterapéutica y Doctrina Médico-Legal** | Ateneo de Psiquiatría")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    delta_acop = f"{(acoplamiento_frontolimbico - 80.0):.1f}%" if acoplamiento_frontolimbico < 70.0 else "Basal Estable"
    st.metric(
        label="Acoplamiento Frontolímbico (dlPFC ➔ Amígdala)",
        value=f"{acoplamiento_frontolimbico:.1f} %",
        delta=delta_acop,
        delta_color="normal" if acoplamiento_frontolimbico >= 70.0 else "inverse",
        help="Eficacia del control inhibitorio top-down ejercido por la corteza prefrontal sobre el complejo basolateral amigdalino."
    )
    st.caption(f"Freno estructural FA: {fa_uncinado:.2f} | Trauma CTQ: {ctq_score}")

with col_m2:
    st.metric(
        label="Disponibilidad Basal Receptores μ-Opioides (MOR)",
        value=f"{tono_mor_basal:.1f} %",
        delta=f"Angustia: {angustia_psiquica:.0f}/100",
        delta_color="inverse",
        help="Disponibilidad de receptores MOR en cíngulo anterior e ínsula. Condiciona la tolerancia neuroquímica al dolor social y al rechazo."
    )
    st.caption("Sustrato PET [¹¹C]carfentanil.")

with col_m3:
    color_rci = "inverse" if rci_index >= 70.0 else "normal"
    st.metric(
        label="Índice RCI Forense (Ley Nac. 26.657)",
        value=f"{rci_index:.1f} %",
        delta="Riesgo Inminente" if rci_index >= 70.0 else "Manejo Ambulatorio",
        delta_color=color_rci,
        help="Cuantificación objetiva de Riesgo Cierto e Inminente para fundamentación conforme al Artículo 20 de la Ley 26.657."
    )
    st.caption("Estratificación de Urgencia vs. Manejo Ambulatorio.")

with col_m4:
    st.metric(
        label="Fenotipo Dimensional AMPD",
        value=fenotipo_ampd[:26] + "...",
        help=fenotipo_ampd + ": " + correlato_neuro
    )
    st.caption(fenotipo_ampd)

st.divider()

# -----------------------------------------------------------------------------
# 5. CONTROL DE NAVEGACIÓN ESTABLE
# -----------------------------------------------------------------------------
modulo = st.radio(
    "Selección de Módulo:",
    [
        "1. Conectoma Funcional fMRI y Desacoplamiento Frontolímbico",
        "2. Neuroquímica del Dolor Social y Fisiopatología de Autolesiones (NSSI)",
        "3. Psicoterapia Basada en Evidencia vs. Farmacoterapia por Síntoma-Blanco",
        "4. Módulo Forense: Imputabilidad (Art. 34 CP) y Dictamen Ley 26.657"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

# -----------------------------------------------------------------------------
# MÓDULO 1: CONECTOMA fMRI Y DINÁMICA DE REDES
# -----------------------------------------------------------------------------
if modulo.startswith("1."):
    st.subheader("Dinámica Conectómica: Colapso del Freno Frontolímbico ante Estrés Relacional")
    st.markdown(
        "Evaluación en tiempo real del balance entre la **Red de Salienccia (SN)** y la **Red de Control Ejecutivo (CEN)**, "
        "modelando el desacoplamiento funcional de la corteza prefrontal dorsolateral (dlPFC) sobre el complejo basolateral amigdalino."
    )

    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        st.markdown("**Respuesta Dinámica de Conectividad ante Estrés Interpersonal Progresivo**")
        estres_eje = np.linspace(0, 100, 120)
        sigmoide_eje = 1.0 / (1.0 + np.exp(-(estres_eje - umbral_quiebre) / 7.5))
        curva_acop = (capacidad_basal_freno * (1.0 - (0.85 * sigmoide_eje)) + (factor_resiliencia_psico * 0.30)) * 100.0
        curva_acop = np.clip(curva_acop, 5.0, 98.0)

        fig_con = go.Figure()

        fig_con.add_trace(go.Scatter(
            x=estres_eje, y=curva_acop,
            mode='lines', name='Acoplamiento dlPFC ➔ Amígdala',
            line=dict(color='#0284C7', width=3.5)
        ))

        fig_con.add_trace(go.Scatter(
            x=[estres_interpersonal], y=[acoplamiento_frontolimbico],
            mode='markers+text', name='Estado Actual Simulado',
            marker=dict(color='#EF4444' if acoplamiento_frontolimbico < 50 else '#10B981', size=13, symbol='diamond'),
            text=[f"Estrés {estres_interpersonal}: {acoplamiento_frontolimbico:.1f}%"],
            textposition="top center",
            textfont=dict(color="#FFFFFF", size=11)
        ))

        fig_con.add_hline(y=40, line_dash="dash", line_color="#EF4444", annotation_text="Zona de Quiebre de Juicio Crítico (Colapso Top-Down)", annotation_font_size=10)

        fig_con.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#0D131F',
            xaxis=dict(title="Magnitud del Estresor Interpersonal de Apego (0-100)", gridcolor='#1E293B'),
            yaxis=dict(title="Acoplamiento Inhibitorio Frontolímbico (%)", gridcolor='#1E293B', range=[0, 105]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=20, b=20),
            height=360
        )
        st.plotly_chart(fig_con, use_container_width=True, key="fig_conectoma_linea")

    with col_c2:
        st.markdown("**Balance de Activación de Redes Funcionales Mayores (fMRI BOLD)**")
        redes_nombres = [
            "Red de Salienccia (SN / Ínsula-dACC)",
            "Red de Control Ejecutivo (CEN / dlPFC)",
            "Red por Defecto (DMN / vmPFC-Precúneo)",
            "Amígdala Basolateral (Reactividad Afectiva)"
        ]
        val_amigdala = float(np.clip(100.0 - acoplamiento_frontolimbico + (labilidad_afectiva * 0.25), 10.0, 100.0))
        val_dmn = float(np.clip(50.0 + (diatesis_trauma * 30.0) - (factor_resiliencia_psico * 15.0), 20.0, 95.0))
        valores_redes = [actividad_sn, actividad_cen, val_dmn, val_amigdala]

        colores_redes = ['#F59E0B', '#0284C7', '#8B5CF6', '#EF4444']

        fig_redes = go.Figure(go.Bar(
            x=valores_redes, y=redes_nombres, orientation='h',
            marker=dict(color=colores_redes, line=dict(color='#1E293B', width=1)),
            text=[f"{v:.1f}%" for v in valores_redes],
            textposition='outside',
            textfont=dict(color="#FFFFFF", size=11)
        ))

        fig_redes.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#0D131F',
            xaxis=dict(title="Nivel de Activación / Reclutamiento Funcional (%)", gridcolor='#1E293B', range=[0, 115]),
            yaxis=dict(gridcolor='#1E293B', autorange="reversed"),
            margin=dict(l=20, r=30, t=10, b=20),
            height=360
        )
        st.plotly_chart(fig_redes, use_container_width=True, key="fig_redes_bar")

    st.info(
        "**CORRELATO BIOMÉDICO DEL CIRCUITO:**\n\n"
        f"* **Integridad del Fascículo Uncinado (FA: {fa_uncinado:.2f}):** Limita físicamente la velocidad de transmisión axonal de la corteza prefrontal hacia el polo temporal y la amígdala.\n"
        f"* **Diátesis por Adversidad Temprana (CTQ: {ctq_score}):** Promueve una hipertrofia funcional de los núcleos basolaterales de la amígdala con menor densidad de receptores glucocorticoides de retroalimentación negativa.\n"
        f"* **Intervención Terapéutica Actual:** {desc_psico}"
    )

# -----------------------------------------------------------------------------
# MÓDULO 2: NEUROQUÍMICA DEL DOLOR SOCIAL Y AUTOLESIONES (NSSI)
# -----------------------------------------------------------------------------
elif modulo.startswith("2."):
    st.subheader("Sustrato Neuroquímico del Dolor Social y las Conductas Autolesivas (NSSI)")
    st.markdown(
        "Modelado farmacodinámico basado en estudios PET con radiotrazador selectivo de receptores opioides **[¹¹C]carfentanil** "
        "(Prossin et al., *Am J Psychiatry* 2010; Schmahl et al., *Neuropsychopharmacology* 2012)."
    )

    col_o1, col_o2 = st.columns([1, 1])

    with col_o1:
        st.markdown("**Cinética de Angustia y Pulso Compensatorio de β-Endorfinas tras Injuria Tisular**")
        tiempo_min = np.linspace(-15, 60, 150)
        angustia_curva = []
        for t in tiempo_min:
            if t < 0:
                angustia_curva.append(angustia_psiquica)
            elif t <= 5:
                # Caída abrupta por rescate de endorfinas inducido por el dolor físico
                alivio = angustia_psiquica * 0.70 * (t / 5.0)
                angustia_curva.append(angustia_psiquica - alivio)
            else:
                # Retorno progresivo a la línea de base disfórica por degradación de neuropéptidos
                val_base = angustia_psiquica * 0.30
                recup = (angustia_psiquica - val_base) * (1.0 - np.exp(-(t - 5.0) / 18.0))
                angustia_curva.append(val_base + recup)

        fig_opioide = go.Figure()

        fig_opioide.add_trace(go.Scatter(
            x=tiempo_min, y=angustia_curva,
            mode='lines', name='Curva de Sufrimiento Psíquico / Disforia',
            line=dict(color='#EF4444', width=3.5)
        ))

        fig_opioide.add_vline(x=0, line_dash="dot", line_color="#F59E0B", annotation_text="Injuria Tisular Aguda (NSSI)", annotation_font_size=10)

        fig_opioide.add_vrect(
            x0=0, x1=15, fillcolor="rgba(16, 185, 129, 0.12)",
            layer="below", line_width=0,
            annotation_text="Ventana de Analgesia Afectiva (Descarga Endorfínica)",
            annotation_position="top right",
            annotation_font=dict(color="#10B981", size=10)
        )

        fig_opioide.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#0D131F',
            xaxis=dict(title="Línea Temporal (Minutos relativos a la conducta autolesiva)", gridcolor='#1E293B'),
            yaxis=dict(title="Intensidad de Angustia / Dolor Afectivo (%)", gridcolor='#1E293B', range=[0, 110]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=20, b=20),
            height=360
        )
        st.plotly_chart(fig_opioide, use_container_width=True, key="fig_opioide_curva")

    with col_o2:
        st.markdown("**Bases Fisiopatológicas: Por qué el Dolor Físico Suprime el Dolor Afectivo**")
        st.markdown(
            "1. **Superposición Neuroanatómica del Dolor:** La corteza cingulada anterior dorsal (dACC) y la ínsula anterior procesan "
            "tanto la aferencia nociceptiva somática como la experiencia de exclusión, abandono e invalidación vincular.\n\n"
            "2. **Déficit Tónico de Endorfinas:** En el fenotipo con alta labilidad afectiva, la disponibilidad basal de receptores MOR es deficitaria. "
            "El paciente experimenta el rechazo interpersonal como una agresión biológica intolerable.\n\n"
            "3. **Rescate Alostático Disfuncional:** El corte tisular o la quemadura recluta una cascada masiva de β-endorfinas y encefalinas destinadas "
            "a mitigar la noxa física periférica. Estas moléculas inundan los receptores MOR de la ínsula, apagando secundariamente la angustia psíquica.\n\n"
            "4. **Implicancia Clínica Ineludible:** La conducta autolesiva no suicida (NSSI) es un mecanismo disfuncional de autorregulación química ante un "
            "aparato neuroendocrino en colapso, no un mero intento manipulativo secundario."
        )

    st.success(
        f"**ESTADO NEUROQUÍMICO ACTUAL:** Disponibilidad basal de receptores MOR calculada en {tono_mor_basal:.1f}%. "
        f"Nivel actual de sufrimiento psíquico derivado del estresor relacional: {angustia_psiquica:.1f}/100. "
        "En este punto crítico, las intervenciones verbales abstractas resultan ineficaces debido al bloqueo prefrontal; "
        "se requieren técnicas conductuales de choque somatosensorial no lesivo (hielo, activación vagal por reflejo de inmersión en DBT) "
        "para inducir neuromodulación sin daño tisular."
    )

# -----------------------------------------------------------------------------
# MÓDULO 3: PSICOTERAPIA BASADA EN EVIDENCIA VS. PSICOFARMACOLOGÍA TRASLACIONAL
# -----------------------------------------------------------------------------
elif modulo.startswith("3."):
    st.subheader("Tratamiento Basado en Evidencia: Neuroplasticidad Psicoterapéutica y Racionalización Farmacológica")
    st.caption("Convergencia entre Guías de Práctica Clínica Internacionales (NICE CG78, WFSBP, APA) y ensayos controlados de neuroimagen.")

    col_t1, col_t2 = st.columns([1, 1])

    with col_t1:
        st.markdown("**A. Evidencia de Neuroplasticidad Inducida por Psicoterapia Manualizada**")
        st.markdown(
            "Los ensayos clínicos aleatorizados con neuroimagen funcional pre y post tratamiento demuestran cambios microestructurales y de conectividad:\n\n"
            "* **Terapia Dialéctico Conductual (DBT / Marsha Linehan):** "
            "Meta-análisis Cochrane (Storebø et al., 2020) valida reducción del 50-70% en NSSI e internaciones de urgencia. "
            "Estudios fMRI (Schmitt et al., 2016) demuestran incremento en la activación de la corteza prefrontal ventrolateral (vlPFC) "
            "y atenuación sostenida del complejo amigdalino ante estímulos aversivos.\n\n"
            "* **Tratamiento Basado en Mentalización (MBT / Bateman & Fonagy):** "
            "Restaura la actividad en la unión temporoparietal (TPJ) y la corteza prefrontal medial (mPFC). Evita que el paciente regrese "
            "a modos pre-mentalizadores (*equivalencia psíquica* y *modo teleológico*) cuando se activa el sistema de apego.\n\n"
            "* **Psicoterapia Focalizada en la Transferencia (TFP / Kernberg & Clarkin):** "
            "Evidencia neurobiológica de reorganización en la Red por Defecto (DMN), permitiendo la integración de representaciones "
            "disociadas (*splitting*) del self y de las figuras vinculares."
        )

    with col_t2:
        st.markdown("**B. Algoritmo Racional de Síntomas-Blanco (Cero Polifarmacia Ciega)**")
        st.markdown(
            "Las guías internacionales son unánimes: **no existe psicofármaco que modifique la estructura nuclear de un trastorno de la personalidad**. "
            "La medicación solo está justificada como adyuvante temporal circunscrito a síntomas-blanco neurobiológicos:\n\n"
            "1. **Para Labilidad Afectiva Extrema e Hiperreactividad:**\n"
            "   * *Dianas moleculares:* Moduladores glutamatérgicos y estabilizadores de membrana canal-dependientes.\n"
            "   * *Fármacos validados:* Lamotrigina (titulación lenta para evitar síndrome de Stevens-Johnson) o Topiramato. Ácidos grasos Omega-3 (EPA/DHA > 1200 mg/día) para fluidez de membrana.\n\n"
            "2. **Para Desregulación Cognitiva y Micropsicosis Reactiva Transitoria:**\n"
            "   * *Dianas moleculares:* Bloqueo parcial D2 / modulación 5-HT2A mesolímbica.\n"
            "   * *Fármacos validados:* Antipsicóticos atípicos en microdosis (Aripiprazol 2.5-5 mg/d o Quetiapina 25-50 mg/d) por períodos breves (4 a 12 semanas máximo).\n\n"
            "3. **Fármacos con Contraindicación Relativa Formal en Guías:**\n"
            "   * *Benzodiacepinas:* Alto riesgo de desinhibición conductual paradójica, dependencia biológica y letalidad en sobredosis.\n"
            "   * *Antidepresivos Tricíclicos:* Letalidad extrema por cardiotoxicidad ante sobreingesta impulsiva."
        )

    st.warning(
        "**PRINCIPIO DE AUDITORÍA ASISTENCIAL (Lex Artis):** La polifarmacia masiva (sedantes + múltiples antipsicóticos + estabilizadores concurrentes) "
        "carece de respaldo empírico de Nivel 1a. La prescripción responsable exige fijar metas temporales de desescalada y consignar explícitamente "
        "que el pilar terapéutico insustituible es el programa psicoterapéutico estructurado."
    )

# -----------------------------------------------------------------------------
# MÓDULO 4: DOCTRINA FORENSE, IMPUTABILIDAD Y LEY 26.657
# -----------------------------------------------------------------------------
elif modulo.startswith("4."):
    st.subheader("Módulo Forense y Doctrina Jurídico-Sanitaria")
    st.caption("Herramienta estructurada de fundamentación pericial y blindaje de la responsabilidad profesional médica.")

    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        st.markdown("#### 1. Capacidad de Culpabilidad e Imputabilidad (Art. 34 inc. 1 CP Argentino)")
        if acoplamiento_frontolimbico < 25.0 and labilidad_afectiva >= 80:
            st.error(
                "**DICTAMEN PERICIAL SUGERIDO: DISMINUCIÓN SUSTANCIAL TRANSITORIA DE LA CULPABILIDAD**\n\n"
                "* **Estado del Juicio Crítico:** Comprensión de la criminalidad parcialmente conservada en lo formal, pero con "
                "**abolición aguda de la capacidad de dirigir las acciones** debido a un colapso neurofuncional del acoplamiento frontolímbico "
                "secundario a un estresor masivo. Configura el estándar doctrinario de **Trastorno Mental Transitorio Incompleto** "
                "(Atenuante de responsabilidad penal conforme a jurisprudencia consolidada)."
            )
        else:
            st.success(
                "**DICTAMEN PERICIAL SUGERIDO: INDEMNIDAD IMPUTATIVA PLENA**\n\n"
                "* **Estado del Juicio Crítico:** El sujeto conserva la capacidad intelectiva de comprender la antijuridicidad de sus actos "
                "y la facultad volitiva basal de autodeterminación. Los rasgos disociales, el antagonismo o la desinhibición caracterológica "
                "**no configuran enajenación mental ni insuficiencia de las facultades** en los términos del Art. 34 inc. 1 del Código Penal. Imputable."
            )

        st.markdown("---")
        st.markdown("#### 2. Criterio de Riesgo Cierto e Inminente (Art. 20 Ley 26.657)")
        if rci_index >= 70.0:
            st.error(
                f"**CONFIGURA RIESGO CIERTO E INMINENTE (Índice RCI: {rci_index:.1f}%):**\n\n"
                "Concurren elementos de estructuración letal, alta intencionalidad lesiva y ausencia de red de contención eficaz. "
                "**Procede la internación involuntaria de urgencia** por dictamen del equipo interdisciplinario. Debe realizarse en "
                "**Hospital General**, con carácter restrictivo y orientada exclusivamente a la estabilización aguda del riesgo vital inmediato."
            )
        else:
            st.info(
                f"**NO CONFIGURA RIESGO CIERTO E INMINENTE EN TÉRMINOS LEGALES (Índice RCI: {rci_index:.1f}%):**\n\n"
                "La conducta autolesiva o ideación disfuncional responde a un patrón parasuicida crónico de desregulación afectiva sin plan letal estructurado. "
                "**La internación involuntaria asilar está formalmente desaconsejada y contraindicada**: genera dependencia institucional, regresión conductual y "
                "cronificación iatrogénica. Se dictamina indicación de seguimiento ambulatorio intensivo con red vincular corresponsable o dispositivo de Hospital de Día."
            )

    with col_f2:
        st.markdown("#### 3. Minuta Estructurada para Blindaje de la Historia Clínica Digital")
        st.caption("Texto preformateado para asentar en guardia o consultorio externo conforme a la Lex Artis Ad Hoc:")

        txt_acta = f"""HISTORIA CLÍNICA Y DICTAMEN ASISTENCIAL / PERICIAL
Fecha de Evaluación: Contexto de Urgencia Psiquiátrica
Paciente: Evaluación Dimensional de Trastorno de la Personalidad (Cluster B)

1. EXAMEN PSICOPATOLÓGICO Y ESTADO COGNITIVO BASAL:
Al momento de la entrevista, el/la paciente se presenta vigil, orientado/a en tiempo y espacio.
Juicio crítico de la realidad formalmente conservado. No se constatan fenómenos de la serie psicótica
congruentes ni incongruentes con el estado del ánimo, ni ideación delirante primaria estructurada.

2. CORRELATO NEUROBIOLÓGICO Y DINÁMICA DE DESREGULACIÓN:
El cuadro clínico responde a un fenotipo de {fenotipo_ampd}, condicionado por antecedentes de
adversidad temprana (CTQ estimado: {ctq_score}) y fragilidad del freno inhibitorio frontoamigdalino
(Integridad DTI de fascículo uncinado FA: {fa_uncinado:.2f}). Ante estresor relacional agudo, se objetiva
desacoplamiento funcional prefrontal ({acoplamiento_frontolimbico:.1f}%), sustentando la disforia aguda.

3. EVALUACIÓN DE RIESGO SEGÚN LEY NACIONAL DE SALUD MENTAL N° 26.657 (ART. 20):
Índice de Riesgo Cierto e Inminente: {rci_index:.1f}%.
Dictamen: {'Configura criterio estricto de internación involuntaria breve en hospital general.' if rci_index >= 70.0 else 'NO configura riesgo cierto e inminente de muerte inmediata. Se contraindica encierro institucional por riesgo de regresión.'}

4. ESTRATEGIA TERAPÉUTICA RACIONALIZADA (LEX ARTIS):
Pilar terapéutico excluyente: Derivación a programa psicoterapéutico estructurado basado en la evidencia ({psicoterapia_activa.split('(')[0]}).
Farmacoterapia: Circunscrita estrictamente a síntomas-blanco temporales. Se evita polifarmacia sedativa.
Se informa acabadamente a la red vincular sobre pautas de alarma y corresponsabilidad del cuidado."""

        st.text_area("Copia de Dictamen Médico-Legal", value=txt_acta, height=360)