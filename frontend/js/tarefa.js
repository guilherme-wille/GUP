const selectCrianca = document.querySelector("#crianca_id");
const avisoSemCriancas = document.querySelector("#aviso-sem-criancas");
const formTarefa = document.querySelector("#form-tarefa");
const mensagem = document.querySelector("#mensagem");

async function carregarCriancas() {
  const { ok, status, dados } = await apiFetch("/tarefas/criar-info");

  if (status === 401) {
    window.location.href = "login.html";
    return;
  }

  if (!ok) {
    mostrarMensagem(mensagem, dados?.erro || "Erro ao carregar crianças.", "erro");
    return;
  }

  if (!dados.criancas.length) {
    avisoSemCriancas.style.display = "block";
    return;
  }

  selectCrianca.innerHTML =
    '<option value="" disabled selected>Selecione...</option>' +
    dados.criancas.map((c) => `<option value="${c.id}">${c.nome}</option>`).join("");
}

formTarefa.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const dados = {
    titulo: document.querySelector("#titulo").value,
    descricao: document.querySelector("#descricao").value,
    crianca_id: document.querySelector("#crianca_id").value,
    horario_limite: document.querySelector("#horario_limite").value,
    xp_ganho: document.querySelector("#xp_ganho").value,
    moedas_ganha: document.querySelector("#moedas_ganha").value,
    moedas_perda: document.querySelector("#moedas_perda").value,
    moedas_atraso: document.querySelector("#moedas_atraso").value,
  };

  const { ok, dados: resposta } = await apiFetch("/tarefas/criar", {
    method: "POST",
    body: dados,
  });

  if (!ok) {
    mostrarMensagem(mensagem, resposta?.erro || "Erro ao criar tarefa.", "erro");
    return;
  }

  window.location.href = "dashboard.html";
});

carregarCriancas();
