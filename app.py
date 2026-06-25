import streamlit as st
from scenarios import SCENARIOS
from evaluator import evaluate_prompt, NIVEL_COLOR, NIVEL_EMOJI

st.set_page_config(
    page_title="Evaluador de Prompts — Power BI",
    page_icon="📊",
    layout="wide",
)

# CSS
st.markdown("""
<style>
    /* Tarjeta de situación */
    .scenario-card {
        background: #1e2a3a;
        border-left: 4px solid #0078d4;
        padding: 1.2rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
        color: #e8edf2 !important;
    }
    .scenario-card * {
        color: #e8edf2 !important;
    }
    .scenario-card code {
        background: #2d4058 !important;
        color: #7dd3fc !important;
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
        font-size: 0.85em;
    }

    /* Criterios de evaluación */
    .criteria-item {
        padding: 0.4rem 0.7rem;
        border-radius: 6px;
        margin: 0.3rem 0;
        font-size: 0.9rem;
        color: #e8edf2 !important;
    }
    .criteria-ok { background: #1a3d2b; border-left: 3px solid #2ecc71; }
    .criteria-fail { background: #3d1a1a; border-left: 3px solid #e74c3c; }
    .criteria-item * { color: #e8edf2 !important; }

    /* Puntuación */
    .score-circle {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        padding: 1rem;
    }

    /* Caja de consejos */
    .tip-box {
        background: #1a2a3a;
        border: 1px solid #0078d4;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        font-size: 0.88rem;
        margin-top: 1rem;
        color: #e8edf2 !important;
    }
    .tip-box * {
        color: #e8edf2 !important;
    }

    /* Alertas nativas de Streamlit */
    .stAlert p, .stAlert li, .stAlert div {
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Evaluador de Prompts para Power BI")
st.markdown("Selecciona una situación real de negocio, escribe tu prompt y recibe feedback inmediato.")

st.divider()

# Scenario selector
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("1. Elige la situación")
    scenario_options = {
        f"{s['icon']} [{s['department']}] {s['title']}": s for s in SCENARIOS
    }
    selected_label = st.radio(
        "Situaciones disponibles:",
        options=list(scenario_options.keys()),
        label_visibility="collapsed",
    )
    selected = scenario_options[selected_label]

with col_right:
    st.subheader("2. Lee la situación")
    with st.container():
        st.markdown(
            f"<div class='scenario-card'>{selected['situation']}</div>",
            unsafe_allow_html=True,
        )
    st.markdown(f"**🎯 Objetivo:** {selected['goal']}")

st.divider()

# Prompt input
st.subheader("3. Escribe tu prompt")
st.markdown(
    "Redacta el prompt que le darías a una IA (o a un compañero) para resolver esta situación en Power BI."
)

with st.expander("💡 Consejos para un buen prompt", expanded=False):
    st.markdown("""
<div class='tip-box'>

**Un buen prompt para Power BI suele incluir:**

- **Contexto** → ¿Qué datos tienes? ¿Qué tablas y columnas relevantes existen?
- **Objetivo claro** → ¿Qué métrica o visual necesitas exactamente?
- **Formato esperado** → ¿Medida DAX, gráfico, tabla, KPI...?
- **Filtros o dimensiones** → ¿Por qué dimensiones quieres analizar el dato?
- **Restricciones** → ¿Hay condiciones especiales (período, estado, tipo)?

</div>
""", unsafe_allow_html=True)

student_prompt = st.text_area(
    "Tu prompt:",
    height=180,
    placeholder="Escribe aquí tu prompt para resolver la situación...",
    label_visibility="collapsed",
)

col_btn, col_info = st.columns([1, 3])
with col_btn:
    evaluate_btn = st.button("🚀 Evaluar prompt", type="primary", use_container_width=True)
with col_info:
    if not student_prompt.strip():
        st.info("Escribe tu prompt antes de evaluar.")
    elif len(student_prompt.strip()) < 30:
        st.warning("Tu prompt parece muy corto. Intenta ser más específico.")

# Evaluation
if evaluate_btn:
    if not student_prompt.strip():
        st.error("Por favor, escribe un prompt antes de evaluar.")
    elif len(student_prompt.strip()) < 10:
        st.error("El prompt es demasiado corto para evaluarlo.")
    else:
        with st.spinner("Analizando tu prompt con IA..."):
            try:
                result = evaluate_prompt(selected, student_prompt)
            except Exception as e:
                st.error(f"Error al conectar con la API: {e}")
                st.stop()

        st.divider()
        st.subheader("4. Resultados de la evaluación")

        nivel = result.get("nivel", "Competente")
        puntuacion = result.get("puntuacion_total", 0)
        color = NIVEL_COLOR.get(nivel, "#888")
        emoji = NIVEL_EMOJI.get(nivel, "")

        # Score row
        col_score, col_nivel, col_spacer = st.columns([1, 2, 3])
        with col_score:
            st.markdown(
                f"<div class='score-circle' style='color:{color}'>{puntuacion}<span style='font-size:1.2rem'>/100</span></div>",
                unsafe_allow_html=True,
            )
        with col_nivel:
            st.markdown(f"### {emoji} {nivel}")
            st.progress(puntuacion / 100)

        st.markdown("---")

        # Criteria
        col_c, col_fb = st.columns([1, 1])

        with col_c:
            st.markdown("#### ✅ Criterios evaluados")
            for item in result.get("criterios", []):
                css_class = "criteria-ok" if item["cumplido"] else "criteria-fail"
                icon = "✅" if item["cumplido"] else "❌"
                st.markdown(
                    f"<div class='criteria-item {css_class}'>"
                    f"<strong>{icon} {item['nombre']}</strong><br>"
                    f"<small>{item['comentario']}</small>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        with col_fb:
            st.markdown("#### 💪 Fortalezas")
            for f in result.get("fortalezas", []):
                st.markdown(f"- {f}")

            st.markdown("#### 🔧 Oportunidades de mejora")
            for m in result.get("mejoras", []):
                st.markdown(f"- {m}")

        # Improved example
        if result.get("ejemplo_prompt_mejorado"):
            st.markdown("---")
            st.markdown("#### 🌟 Ejemplo de prompt mejorado")
            st.info(result["ejemplo_prompt_mejorado"])

        st.markdown("---")
        st.caption("Evaluación generada por IA · Los resultados son orientativos y pueden variar.")
