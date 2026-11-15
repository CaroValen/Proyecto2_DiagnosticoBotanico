"""Interfaz original del chatbot adaptada para Windows, Git y dos motores."""

import os

import streamlit as st

from conocimiento import SINTOMAS
from motores import diagnosticar_gemini, diagnosticar_prolog

st.set_page_config(page_title="Chatbot Botánico - IA", page_icon="🌿")
st.title("Agente Inteligente de Diagnóstico Botánico")
st.write("Fundamentos de Inteligencia Artificial - Proyecto N° 2")
st.subheader("Configuración del Motor de Inferencia")

motor = st.radio(
    "Selecciona el motor para evaluar los síntomas:",
    ("Motor de Deducción (SWI-Prolog)", "Modelo de Lenguaje (LLM - Gemini)"),
)

api_key = ""
if motor == "Modelo de Lenguaje (LLM - Gemini)":
    api_key = st.text_input(
        "Ingresa tu API Key de Google Gemini:",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
    )

st.write("---")
st.write("Selecciona los síntomas presentes en tu planta:")

preguntas = {
    "hojas_amarillas": "¿Las hojas de tu planta están amarillas?",
    "tierra_humeda": "¿La tierra está muy húmeda o encharcada?",
    "hojas_secas": "¿Las hojas están marrones, crujientes o secas?",
    "tierra_seca": "¿El sustrato está completamente seco?",
    "tallos_estirados": "¿Los tallos están muy largos/estirados buscando luz?",
    "hojas_palidas": "¿Las hojas nuevas nacen muy pequeñas o pálidas?",
    "puntos_blancos": "¿Observas puntos blancos algodonosos pegados en hojas o tallos?",
    "manchas_cafes": "¿Las hojas tienen manchas quemadas de color café en el centro?",
}
assert set(preguntas) == set(SINTOMAS)
sintomas_map = {codigo: st.checkbox(texto) for codigo, texto in preguntas.items()}

if st.button("Consultar Sistema"):
    sintomas_presentes = [nombre for nombre, presente in sintomas_map.items() if presente]

    if not sintomas_presentes:
        st.info("No has seleccionado ningún síntoma.")
    elif "tierra_humeda" in sintomas_presentes and "tierra_seca" in sintomas_presentes:
        st.warning("La tierra no puede estar húmeda y completamente seca a la vez. Corrija la selección.")
    elif motor == "Motor de Deducción (SWI-Prolog)":
        try:
            salida = diagnosticar_prolog(sintomas_presentes)
            st.write("### Salida del Motor Prolog:")
            st.code(salida, language="prolog")
        except (RuntimeError, OSError, ValueError) as exc:
            st.error(f"Error al ejecutar SWI-Prolog: {exc}")
    elif not api_key:
        st.warning("⚠️ Debes ingresar una API Key válida para usar el LLM.")
    else:
        try:
            with st.spinner("Consultando al LLM..."):
                salida = diagnosticar_gemini(sintomas_presentes, api_key)
            st.write("### Salida del Motor LLM:")
            st.success(salida)
        except Exception as exc:
            mensaje = str(exc).replace(api_key, "[clave oculta]")
            st.error(f"Error de conexión con la API del LLM: {mensaje}")
