// Endereço da API: por padrão, o mesmo domínio que serve esta página.
const API_BASE = window.API_BASE || "";

const form = document.getElementById("form");
const campo = document.getElementById("pergunta");
const botao = document.getElementById("enviar");
const contador = document.getElementById("contador");
const resultado = document.getElementById("resultado");
const resposta = document.getElementById("resposta");

campo.addEventListener("input", () => {
  contador.textContent = `${campo.value.length}/1000`;
});

function mostrar(texto, ehErro) {
  resultado.hidden = false;
  resposta.textContent = texto;
  resposta.classList.toggle("erro", ehErro);
}

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const pergunta = campo.value.trim();
  if (!pergunta) {
    mostrar("Digite uma pergunta antes de enviar.", true);
    return;
  }

  botao.disabled = true;
  botao.textContent = "Pensando...";
  mostrar("Consultando a IA...", false);

  try {
    const r = await fetch(`${API_BASE}/perguntar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta }),
    });
    const dados = await r.json();
    if (!r.ok) {
      mostrar(dados.erro || "Erro ao consultar a IA.", true);
    } else {
      mostrar(dados.resposta, false);
    }
  } catch (e) {
    mostrar("Não foi possível conectar ao servidor.", true);
  } finally {
    botao.disabled = false;
    botao.textContent = "Perguntar";
  }
});
