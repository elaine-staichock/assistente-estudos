"""API do Assistente de Estudos (Flask)."""
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

import ia

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
LIMITE_CARACTERES = 1000


def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder=None)

    @app.get("/saude")
    def saude():
        return jsonify({"status": "ok"})

    @app.post("/perguntar")
    def perguntar():
        dados = request.get_json(silent=True) or {}
        pergunta = dados.get("pergunta") if isinstance(dados, dict) else None

        if not isinstance(pergunta, str) or not pergunta.strip():
            return jsonify({"erro": "Envie uma pergunta no campo 'pergunta'."}), 400
        if len(pergunta) > LIMITE_CARACTERES:
            return (
                jsonify({"erro": f"A pergunta deve ter até {LIMITE_CARACTERES} caracteres."}),
                400,
            )

        try:
            resposta = ia.perguntar_ia(pergunta.strip())
        except ia.ErroIA as erro:
            return jsonify({"erro": str(erro)}), 502

        return jsonify({"resposta": resposta})

    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/<path:arquivo>")
    def estaticos(arquivo):
        return send_from_directory(FRONTEND_DIR, arquivo)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
