import pytest
import requests

import ia


class RespostaFalsa:
    def __init__(self, status=200, corpo=None, json_invalido=False):
        self.status_code = status
        self._corpo = corpo
        self._json_invalido = json_invalido

    def json(self):
        if self._json_invalido:
            raise ValueError("json inválido")
        return self._corpo


def resposta_ok(texto):
    return RespostaFalsa(corpo={"candidates": [{"content": {"parts": [{"text": texto}]}}]})


def test_sem_chave_levanta_erro(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ia.ErroIA, match="GEMINI_API_KEY"):
        ia.perguntar_ia("oi")


def test_sucesso_monta_requisicao_correta(monkeypatch):
    capturado = {}

    def post_falso(url, headers, json, timeout):
        capturado.update(url=url, headers=headers, json=json, timeout=timeout)
        return resposta_ok("  Olá!  ")

    monkeypatch.setattr(ia.requests, "post", post_falso)
    monkeypatch.setenv("GEMINI_MODEL", "modelo-teste")

    assert ia.perguntar_ia("Qual a capital do Brasil?", chave="CHAVE_FALSA") == "Olá!"
    assert "modelo-teste:generateContent" in capturado["url"]
    assert capturado["headers"]["x-goog-api-key"] == "CHAVE_FALSA"
    assert capturado["json"]["contents"][0]["parts"][0]["text"] == "Qual a capital do Brasil?"


def test_usa_chave_e_modelo_padrao_do_ambiente(monkeypatch):
    capturado = {}

    def post_falso(url, headers, json, timeout):
        capturado.update(url=url, headers=headers)
        return resposta_ok("ok")

    monkeypatch.setattr(ia.requests, "post", post_falso)
    monkeypatch.setenv("GEMINI_API_KEY", "CHAVE_DO_AMBIENTE")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    ia.perguntar_ia("oi")
    assert capturado["headers"]["x-goog-api-key"] == "CHAVE_DO_AMBIENTE"
    assert ia.MODELO_PADRAO in capturado["url"]


def test_junta_varias_partes(monkeypatch):
    corpo = {"candidates": [{"content": {"parts": [{"text": "A"}, {"text": "B"}]}}]}
    monkeypatch.setattr(ia.requests, "post", lambda *a, **k: RespostaFalsa(corpo=corpo))
    assert ia.perguntar_ia("x", chave="k") == "AB"


def test_falha_de_rede(monkeypatch):
    def post_falso(*a, **k):
        raise requests.ConnectionError("sem rede")

    monkeypatch.setattr(ia.requests, "post", post_falso)
    with pytest.raises(ia.ErroIA, match="contactar"):
        ia.perguntar_ia("x", chave="k")


def test_status_diferente_de_200(monkeypatch):
    monkeypatch.setattr(ia.requests, "post", lambda *a, **k: RespostaFalsa(status=429))
    with pytest.raises(ia.ErroIA, match="429"):
        ia.perguntar_ia("x", chave="k")


@pytest.mark.parametrize(
    "resp",
    [
        RespostaFalsa(corpo={}),
        RespostaFalsa(corpo={"candidates": []}),
        RespostaFalsa(json_invalido=True),
    ],
)
def test_resposta_inesperada(monkeypatch, resp):
    monkeypatch.setattr(ia.requests, "post", lambda *a, **k: resp)
    with pytest.raises(ia.ErroIA, match="inesperada"):
        ia.perguntar_ia("x", chave="k")


def test_resposta_vazia(monkeypatch):
    monkeypatch.setattr(ia.requests, "post", lambda *a, **k: resposta_ok("   "))
    with pytest.raises(ia.ErroIA, match="vazia"):
        ia.perguntar_ia("x", chave="k")
