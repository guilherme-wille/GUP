(async () => {
  const usuario = await exigirLogin();
  if (!usuario) return;
})();

const formFamilia = document.querySelector("#form-familia");
const mensagem = document.querySelector("#mensagem");

formFamilia.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const dados = {
    nome: document.querySelector("#nome").value,
    pin: document.querySelector("#pin").value,
  };

  const { ok, dados: resposta } = await apiFetch("/contas/criar", {
    method: "POST",
    body: dados,
  });

  if (!ok) {
    mostrarMensagem(mensagem, resposta?.erro || "Erro ao criar conta.", "erro");
    return;
  }

  window.location.href = "dashboard.html";
});
