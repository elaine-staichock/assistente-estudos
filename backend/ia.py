"""Cliente da IA Generativa (Google Gemini via API REST)."""
import os

import requests

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
MODELO_PADRAO = "gemini-3.5-flash"
INSTRUCAO = (
    "Você é um assistente de estudos para estudantes brasileiros. "
    "Responda em português, de forma clara, didática e objetiva, "
    "com exemplos curtos quando ajudar. Se não souber, diga que não sabe."
)


class ErroIA(Exception):
    """Falha ao obter resposta da IA."""


def perguntar_ia(pergunta, chave=None, modelo=None, timeout=30):
    chave = chave or os.getenv("GEMINI_API_KEY")
    if not chave:
        raise ErroIA("Chave da IA (GEMINI_API_KEY) não configurada no servidor.")
    modelo = modelo or os.getenv("GEMINI_MODEL") or MODELO_PADRAO

    corpo = {
        "systemInstruction": {"parts": [{"text": INSTRUCAO}]},
        "contents": [{"role": "user", "parts": [{"text": pergunta}]}],
    }
    try:
        resp = requests.post(
            API_URL.format(modelo=modelo),
            headers={"x-goog-api-key": chave, "Content-Type": "application/json"},
            json=corpo,
            timeout=timeout,
        )
    except requests.RequestException as erro:
        raise ErroIA("Não foi possível contactar a IA. Tente novamente.") from erro

    if resp.status_code != 200:
        raise ErroIA(f"A IA retornou erro (HTTP {resp.status_code}).")

    try:
        partes = resp.json()["candidates"][0]["content"]["parts"]
        texto = "".join(p.get("text", "") for p in partes).strip()
    except (KeyError, IndexError, TypeError, ValueError) as erro:
        raise ErroIA("Resposta inesperada da IA.") from erro

    if not texto:
        raise ErroIA("A IA devolveu uma resposta vazia.")
    return texto
