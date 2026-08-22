const formCadastro = document.querySelector("#form-cadastro");
const mensagem = document.querySelector("#mensagem");

formCadastro.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const dados = {
    nome: document.querySelector("#nome").value,
    email: document.querySelector("#email").value,
    senha: document.querySelector("#senha").value,
    data_nasc: document.querySelector("#data_nasc").value,
  };

  const { ok, dados: resposta } = await apiFetch("/usuarios/cadastro", {
    method: "POST",
    body: dados,
  });

  if (!ok) {
    mostrarMensagem(mensagem, resposta?.erro || "Erro ao cadastrar.", "erro");
    return;
  }

  window.location.href = "dashboard.html";
});
