"""Conectores independientes para SWI-Prolog y Gemini."""

import subprocess
import time
from pathlib import Path

from conocimiento import REGLAS, SINTOMAS

PROLOG = Path(__file__).resolve().parent / "chatbot_plantas.pl"


def diagnosticar_prolog(sintomas: list[str]) -> str:
    desconocidos = set(sintomas) - SINTOMAS.keys()
    if desconocidos:
        raise ValueError(f"Síntomas desconocidos: {', '.join(sorted(desconocidos))}")

    # Los átomos provienen únicamente de la lista blanca SINTOMAS.
    lista_prolog = "[" + ",".join(sintomas) + "]"
    comando = ["swipl", "-q", "-s", str(PROLOG), "-g", f"diagnosticar({lista_prolog})", "-t", "halt"]
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=15, check=False)
    except FileNotFoundError as exc:
        raise RuntimeError("No se encontró SWI-Prolog. Instálalo y verifica el comando 'swipl'.") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("El motor Prolog tardó demasiado en responder.") from exc

    if resultado.returncode != 0:
        raise RuntimeError(f"Prolog terminó con error: {resultado.stderr.strip() or resultado.returncode}")
    return resultado.stdout.strip()


def diagnosticar_gemini(sintomas: list[str], api_key: str) -> str:
    if not api_key.strip():
        raise ValueError("Falta la clave de API de Gemini.")
    if set(sintomas) - SINTOMAS.keys():
        raise ValueError("Se recibió un síntoma no reconocido.")

    from google import genai

    conocimiento = "\n".join(
        f"- {nombre}: síntomas necesarios = {', '.join(requisitos)}. Recomendación: {recomendacion}"
        for nombre, (requisitos, recomendacion) in REGLAS.items()
    )
    prompt = (
        "Eres un agente experto en botánica de interior. Tu tarea es diagnosticar "
        "el problema de una planta basado estrictamente en el siguiente modelo de conocimiento. "
        "Usa SOLAMENTE las siguientes reglas; no inventes enfermedades ni síntomas. "
        "Una regla se cumple únicamente si están presentes TODOS sus síntomas. "
        "Enumera todas las reglas que se cumplen; si ninguna se cumple, dilo claramente. "
        "Analiza los síntomas, indica los diagnósticos que correspondan y entrega "
        "las recomendaciones de forma clara y directa. "
        "No presentes el diagnóstico como certeza. Responde en español.\n\n"
        f"Reglas:\n{conocimiento}\n\n"
        f"Síntomas presentes: {', '.join(sintomas) if sintomas else 'ninguno'}"
    )
    cliente = genai.Client(api_key=api_key)
    respuesta = None
    for intento in range(3):
        try:
            respuesta = cliente.models.generate_content(model="gemini-3.5-flash-lite", contents=prompt)
            break
        except genai.errors.ServerError as exc:
            if exc.code not in (500, 502, 503, 504):
                raise
            if intento == 2:
                raise RuntimeError("Gemini está temporalmente ocupado; vuelve a intentar más tarde.") from exc
            time.sleep(2 ** intento)
    if respuesta is None or not respuesta.text:
        raise RuntimeError("Gemini no devolvió texto para esta consulta.")
    return respuesta.text
