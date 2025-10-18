import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
APERTUS_API_KEY = os.getenv('APERTUS_API_KEY')


# ---------------- GEMINI ----------------
def ask_gemini(prompt: str, instructions: str = None, api_key=GEMINI_API_KEY):
    """
    Envía un prompt al modelo Gemini y devuelve respuesta y status.
    Si se pasan 'instructions', se incluyen como rol de administrador para guiar la respuesta.
    otro modelo chido es: gemini-2.5-flash-lite
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }

    # Si hay instrucciones, las ponemos al inicio del prompt
    full_prompt = f"{instructions}\n\n{prompt}" if instructions else prompt

    data = {
        "contents": [
            {"parts": [{"text": full_prompt}]}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    status = response.status_code

    print(f"\n--- GEMINI | STATUS: {status} ---")

    try:
        resp_json = response.json()
        print(json.dumps(resp_json, indent=4, ensure_ascii=False))
        text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Error al parsear JSON:", e)
        text = response.text

    print(f"\nRespuesta:\n{text}")
    return status, text


# ---------------- APERTUS ----------------
def ask_apertus(prompt: str, instructions: str = None, api_key=APERTUS_API_KEY, model="swiss-ai/apertus-8b-instruct"):
    """
    Envía un prompt al modelo Apertus y devuelve respuesta y status.
    Si se pasan 'instructions', se incluyen como rol de administrador para guiar la respuesta.
    """
    url = "https://api.publicai.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "MiApp/1.0",
        "Content-Type": "application/json"
    }

    messages = []
    if instructions:
        messages.append({"role": "system", "content": instructions})
    messages.append({"role": "user", "content": prompt})

    data = {
        "model": model,
        "messages": messages,
        "max_tokens": 200,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    status = response.status_code

    print(f"\n--- APERTUS | STATUS: {status} ---")

    try:
        resp_json = response.json()
        print(json.dumps(resp_json, indent=4, ensure_ascii=False))
        text = resp_json["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error al parsear JSON:", e)
        text = response.text

    print(f"\nRespuesta:\n{text}")
    return status, text