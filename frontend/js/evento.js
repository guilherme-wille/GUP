const formEvento = document.querySelector("#form-evento");
const mensagem = document.querySelector("#mensagem");

formEvento.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const dados = {
    titulo: document.querySelector("#titulo").value,
    descricao: document.querySelector("#descricao").value,
    data: document.querySelector("#data").value,
  };

  const { ok, dados: resposta } = await apiFetch("/eventos/", {
    method: "POST",
    body: dados,
  });

  if (!ok) {
    mostrarMensagem(mensagem, resposta?.erro || "Erro ao criar evento.", "erro");
    return;
  }

  window.location.href = "dashboard.html";
});
