// Antes o home_controller.py fazia esse roteamento no servidor (redirect
// para login ou dashboard). Agora, sem Jinja/redirects do Flask, essa
// decisão simples é feita no próprio frontend, consultando GET /usuarios/me.
(async () => {
  const { dados } = await apiFetch("/usuarios/me");

  if (!dados || !dados.logado) {
    window.location.href = "login.html";
    return;
  }

  if (!dados.tem_familia) {
    window.location.href = "lobby.html";
    return;
  }

  window.location.href = "dashboard.html";
})();
