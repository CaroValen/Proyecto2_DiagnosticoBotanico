# Chatbot de diagnóstico botánico

Proyecto N°2 de Fundamentos de IA: dos motores de diagnóstico para plantas de interior (SWI-Prolog y Gemini), con una interfaz Streamlit.
Hecho por: 
Carolina Valenzuela
Marco Fuentealba
Dante Ojeda

## Requisitos

- Python 3.10 o superior.
- SWI-Prolog instalado y disponible como comando `swipl`.
- Clave de Gemini para usar el motor LLM (el modo Prolog no necesita conexión ni clave).

## Ejecutar localmente (sin Colab)

Desde esta carpeta:

```bash
python -m venv .venv
```

Activar el entorno:

Linux/macOS: `source .venv/bin/activate`
Windows PowerShell: `.venv\Scripts\Activate.ps1`

Instalar dependencias y ejecutar:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abrir la dirección local que muestra Streamlit (normalmente `http://localhost:8501`). Para Gemini, escribir la clave en el campo protegido o configurar `GEMINI_API_KEY` como variable de entorno. NO subir claves a Git

## Pruebas

```bash
python -m unittest discover -s tests -v
```

```bash
swipl -q -s chatbot_plantas.pl -g 'diagnosticar([puntos_blancos])' -t halt
```
