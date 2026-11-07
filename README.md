# 📚 Assistente de Estudos com IA Generativa

[![CI](https://github.com/elaine-staichock/assistente-estudos/actions/workflows/ci.yml/badge.svg)](https://github.com/elaine-staichock/assistente-estudos/actions/workflows/ci.yml)

Mini-aplicação web de perguntas e respostas: o usuário digita uma dúvida de estudo e a IA generativa (**Google Gemini**) responde na tela.

🔗 **Aplicação online:** https://SEU-APP.onrender.com
🎥 **Vídeo de demonstração:** COLE_O_LINK_AQUI

## Tecnologias

- **Backend:** Python 3.12 + Flask (API REST) + Gunicorn
- **IA:** Google Gemini (API REST, modelo configurável)
- **Frontend:** HTML, CSS e JavaScript puro (servido pelo próprio backend)
- **Testes:** pytest + pytest-cov (IA simulada com mock)
- **CI/CD:** GitHub Actions · **Deploy:** Render

## Estrutura

```
├── backend/            # API Flask, cliente da IA e testes
│   ├── app.py          # endpoints e entrega do frontend
│   ├── ia.py           # chamada ao Gemini
│   └── tests/
├── frontend/           # interface web (index.html, style.css, script.js)
├── .github/workflows/  # pipeline de CI
├── .env.example        # modelo das variáveis de ambiente
└── render.yaml         # configuração de deploy
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/saude` | Verifica se a API está no ar → `{"status": "ok"}` |
| `POST` | `/perguntar` | Recebe `{"pergunta": "..."}` e devolve `{"resposta": "..."}` |

Erros: `400` (pergunta vazia/inválida/maior que 1000 caracteres) e `502` (falha da IA).

```bash
curl -X POST http://localhost:5000/perguntar \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "O que é fotossíntese?"}'
```

## Como rodar localmente

```bash
git clone https://github.com/SEU_USUARIO/assistente-estudos.git
cd assistente-estudos/backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

cp ../.env.example .env      # edite e coloque sua GEMINI_API_KEY
python app.py                # abra http://localhost:5000
```

Chave gratuita do Gemini: <https://aistudio.google.com/apikey>

## Testes

```bash
cd backend
pytest --cov --cov-fail-under=70
```

A chamada à IA é simulada (mock), então os testes não usam internet nem chave real.

## Deploy (Render)

1. Suba o repositório para o GitHub.
2. No Render: **New → Blueprint** e selecione o repositório (usa o `render.yaml`).
3. Defina a variável de ambiente `GEMINI_API_KEY` no painel do Render.
4. Após o deploy, teste `https://SEU-APP.onrender.com/saude`.

## Segurança

A chave da API fica **apenas** em variável de ambiente (`.env` local, painel do Render em produção). O `.env` está no `.gitignore` e nenhum segredo é versionado.
