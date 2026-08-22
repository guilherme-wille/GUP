(async () => {
  const usuario = await exigirLogin();
  if (!usuario) return;
})();

const formEntrar = document.querySelector("#form-entrar-familia");
const mensagem = document.querySelector("#mensagem");

formEntrar.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const dados = {
    email_dono: document.querySelector("#email_dono").value,
    pin: document.querySelector("#pin").value,
  };

  const { ok, dados: resposta } = await apiFetch("/contas/login", {
    method: "POST",
    body: dados,
  });

  if (!ok) {
    mostrarMensagem(mensagem, resposta?.erro || "Erro ao entrar na família.", "erro");
    return;
  }

  window.location.href = "dashboard.html";
});
