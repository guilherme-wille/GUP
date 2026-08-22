const tituloFamilia = document.querySelector("#titulo-familia");
const listaMembros = document.querySelector("#lista-membros");
const mensagem = document.querySelector("#mensagem");

async function carregarConta() {
  const { ok, status, dados } = await apiFetch("/contas/info");

  if (status === 401) {
    window.location.href = "login.html";
    return;
  }

  if (!ok) {
    listaMembros.innerHTML = "";
    mostrarMensagem(mensagem, dados?.erro || "Erro ao carregar a família.", "erro");
    return;
  }

  tituloFamilia.textContent = `Família: ${dados.nome_familia}`;

  if (!dados.membros.length) {
    listaMembros.innerHTML = "<p>Nenhuma pessoa encontrada nesta família.</p>";
    return;
  }

  listaMembros.innerHTML = `<ul>${dados.membros
    .map((m) => `<li><strong>${m.nome}</strong> <em>(${m.tipo_usuario})</em></li>`)
    .join("")}</ul>`;
}

carregarConta();
