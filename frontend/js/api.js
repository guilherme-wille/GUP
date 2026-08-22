// Endereço base da API Flask. Ajuste aqui se o backend rodar em outra porta/host.
const API_URL = "http://127.0.0.1:5000";

/**
 * Wrapper em volta do fetch para conversar com a API do GUP.
 * - Sempre manda/recebe cookies de sessão (credentials: "include").
 * - Sempre manda/recebe JSON (exceto quando body é FormData, usado no
 *   upload da foto de comprovação da tarefa).
 */
async function apiFetch(caminho, opcoes = {}) {
  const configuracao = {
    method: opcoes.method || "GET",
    credentials: "include",
    headers: {},
  };

  if (opcoes.body instanceof FormData) {
    configuracao.body = opcoes.body;
  } else if (opcoes.body !== undefined) {
    configuracao.headers["Content-Type"] = "application/json";
    configuracao.body = JSON.stringify(opcoes.body);
  }

  const resposta = await fetch(`${API_URL}${caminho}`, configuracao);

  let dados = null;
  try {
    dados = await resposta.json();
  } catch (erro) {
    dados = null;
  }

  return { ok: resposta.ok, status: resposta.status, dados };
}

function mostrarMensagem(elemento, texto, tipo) {
  if (!elemento) return;
  elemento.textContent = texto;
  elemento.className = `mensagem ${tipo}`;
}

/** Garante que existe um usuário logado; senão, manda para o login. */
async function exigirLogin() {
  const { dados } = await apiFetch("/usuarios/me");
  if (!dados || !dados.logado) {
    window.location.href = "login.html";
    return null;
  }
  return dados;
}

function formatarData(isoString) {
  if (!isoString) return "—";
  const data = new Date(isoString);
  return data.toLocaleString("pt-BR");
}
