const formLogin = document.querySelector("#form-login");
const mensagem = document.querySelector("#mensagem");

formLogin.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const email = document.querySelector("#email").value;
  const senha = document.querySelector("#senha").value;

  const { ok, dados } = await apiFetch("/usuarios/login", {
    method: "POST",
    body: { email, senha },
  });

  if (!ok) {
    mostrarMensagem(mensagem, dados?.erro || "Erro ao entrar.", "erro");
    return;
  }

  window.location.href = "dashboard.html";
});
