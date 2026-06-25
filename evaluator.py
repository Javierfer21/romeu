import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
except Exception:
    api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key)


SYSTEM_PROMPT = """Eres un evaluador experto en Power BI y en la técnica de prompting.
Tu tarea es evaluar la calidad del prompt que ha escrito un alumno para resolver una situación
de negocio en Power BI.

Debes evaluar el prompt según los criterios que se te proporcionen y devolver SIEMPRE
un JSON válido con exactamente esta estructura, sin texto adicional fuera del JSON:

{
  "puntuacion_total": <número entero de 0 a 100>,
  "nivel": "<Principiante|En desarrollo|Competente|Avanzado|Experto>",
  "criterios": [
    {
      "nombre": "<nombre del criterio>",
      "cumplido": <true|false>,
      "comentario": "<explicación breve de por qué se cumple o no>"
    }
  ],
  "fortalezas": ["<fortaleza 1>", "<fortaleza 2>"],
  "mejoras": ["<mejora 1>", "<mejora 2>", "<mejora 3>"],
  "ejemplo_prompt_mejorado": "<versión mejorada del prompt del alumno, manteniendo su estilo>"
}

Criterios de nivel:
- 0-39: Principiante
- 40-59: En desarrollo
- 60-74: Competente
- 75-89: Avanzado
- 90-100: Experto

Sé constructivo, específico y orientado al aprendizaje. El ejemplo mejorado debe ser
realista y educativo, no perfecto al 100%."""


def evaluate_prompt(scenario: dict, student_prompt: str) -> dict:
    criteria_text = "\n".join(
        f"  {i+1}. {c}" for i, c in enumerate(scenario["criteria"])
    )

    user_message = f"""
## Situación planteada al alumno
Departamento: {scenario['department']}
Tarea: {scenario['title']}
Objetivo: {scenario['goal']}

## Criterios de evaluación (cada uno vale {100 // len(scenario['criteria'])} puntos aprox.)
{criteria_text}

## Prompt escrito por el alumno
\"\"\"
{student_prompt}
\"\"\"

Evalúa el prompt según los criterios anteriores y devuelve el JSON de evaluación.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code blocks if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    return json.loads(raw)


NIVEL_COLOR = {
    "Principiante": "#e74c3c",
    "En desarrollo": "#e67e22",
    "Competente": "#f1c40f",
    "Avanzado": "#2ecc71",
    "Experto": "#27ae60",
}

NIVEL_EMOJI = {
    "Principiante": "🔴",
    "En desarrollo": "🟠",
    "Competente": "🟡",
    "Avanzado": "🟢",
    "Experto": "🌟",
}
