import pytest

import app as modulo_app
import ia


@pytest.fixture
def client():
    flask_app = modulo_app.create_app()
    flask_app.config["TESTING"] = True
    return flask_app.test_client()


def test_saude(client):
    r = client.get("/saude")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_perguntar_sucesso_com_ia_simulada(client, monkeypatch):
    monkeypatch.setattr(ia, "perguntar_ia", lambda p: f"Resposta simulada para: {p}")
    r = client.post("/perguntar", json={"pergunta": "  O que é DNA?  "})
    assert r.status_code == 200
    assert r.get_json() == {"resposta": "Resposta simulada para: O que é DNA?"}


@pytest.mark.parametrize("corpo", [{}, {"pergunta": ""}, {"pergunta": "   "}, {"pergunta": 123}, [1, 2]])
def test_perguntar_invalida(client, corpo):
    r = client.post("/perguntar", json=corpo)
    assert r.status_code == 400
    assert "erro" in r.get_json()


def test_perguntar_sem_json(client):
    r = client.post("/perguntar", data="não é json")
    assert r.status_code == 400


def test_perguntar_muito_longa(client):
    r = client.post("/perguntar", json={"pergunta": "a" * 1001})
    assert r.status_code == 400


def test_perguntar_erro_da_ia_vira_502(client, monkeypatch):
    def falha(_):
        raise ia.ErroIA("IA indisponível")

    monkeypatch.setattr(ia, "perguntar_ia", falha)
    r = client.post("/perguntar", json={"pergunta": "oi"})
    assert r.status_code == 502
    assert r.get_json() == {"erro": "IA indisponível"}


def test_serve_frontend(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Assistente de Estudos" in r.data
    r.close()
    css = client.get("/style.css")
    assert css.status_code == 200
    css.close()


def test_arquivo_inexistente_404(client):
    assert client.get("/nao-existe.txt").status_code == 404
