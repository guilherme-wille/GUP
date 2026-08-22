const filtroCriancas = document.querySelector("#filtro-criancas");
const conteudoHistorico = document.querySelector("#conteudo-historico");
const mensagem = document.querySelector("#mensagem");

function idCriancaDaUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("crianca_id");
}

function renderizarFiltro(criancas, ehResponsavel, criancaAtualId) {
  if (!ehResponsavel || !criancas.length) {
    filtroCriancas.innerHTML = "";
    return;
  }

  filtroCriancas.innerHTML =
    "<strong>Ver histórico de:</strong> " +
    criancas
      .map(
        (c) =>
          `<a class="chip ${c.id == criancaAtualId ? "ativo" : ""}" href="historico.html?crianca_id=${c.id}">${c.nome}</a>`
      )
      .join(" ");
}

function renderizarAjuste(crianca) {
  return `
    <div class="card">
      <h4>Ajustar moedas de ${crianca.nome}</h4>
      <form id="form-ajuste">
        <label><input type="radio" name="tipo_ajuste" value="adicionar" checked> Adicionar</label>
        <label><input type="radio" name="tipo_ajuste" value="remover"> Retirar</label>

        <label for="valor-ajuste">Quantidade de moedas</label>
        <input type="number" id="valor-ajuste" min="1" required>

        <label for="motivo-ajuste">Motivo</label>
        <input type="text" id="motivo-ajuste" placeholder="Ex: Ajudou a organizar a garagem" required>

        <button type="submit">Confirmar ajuste</button>
      </form>
    </div>
  `;
}

function renderizarTabela(historico) {
  if (!historico.length) {
    return "<p>Nenhuma movimentação registrada ainda.</p>";
  }

  const linhas = historico
    .map((item) => {
      const entrada = item.valor > 0;
      return `
        <tr>
          <td class="${entrada ? "entrada" : "saida"}">${entrada ? "ENTRADA" : "SAÍDA"}</td>
          <td>${entrada ? item.valor : -item.valor} moedas</td>
          <td>${item.descricao || ""}</td>
          <td>${item.origem}</td>
          <td>${formatarData(item.data_hora)}</td>
        </tr>
      `;
    })
    .join("");

  return `
    <table>
      <tr><th>Tipo</th><th>Valor</th><th>Motivo</th><th>Origem</th><th>Data</th></tr>
      ${linhas}
    </table>
  `;
}

async function carregarHistorico() {
  const criancaId = idCriancaDaUrl();
  const caminho = criancaId ? `/historico?crianca_id=${criancaId}` : "/historico";

  const { ok, status, dados } = await apiFetch(caminho);

  if (status === 401) {
    window.location.href = "login.html";
    return;
  }

  if (!ok) {
    conteudoHistorico.innerHTML = "";
    mostrarMensagem(mensagem, dados?.erro || "Erro ao carregar histórico.", "erro");
    return;
  }

  renderizarFiltro(dados.criancas, dados.eh_responsavel, dados.crianca ? dados.crianca.id : null);

  if (!dados.crianca) {
    conteudoHistorico.innerHTML = "<p>Nenhuma criança encontrada.</p>";
    return;
  }

  let html = `<h3>Extrato de: ${dados.crianca.nome} (Saldo: ${dados.crianca.moedas} moedas)</h3>`;

  if (dados.eh_responsavel) {
    html += renderizarAjuste(dados.crianca);
  }

  html += renderizarTabela(dados.historico);
  conteudoHistorico.innerHTML = html;

  const formAjuste = document.querySelector("#form-ajuste");
  if (formAjuste) {
    formAjuste.addEventListener("submit", async (evento) => {
      evento.preventDefault();

      const tipoAjuste = formAjuste.querySelector('input[name="tipo_ajuste"]:checked').value;
      const valor = document.querySelector("#valor-ajuste").value;
      const motivo = document.querySelector("#motivo-ajuste").value;

      const { ok: okAjuste, dados: respostaAjuste } = await apiFetch(
        `/criancas/${dados.crianca.id}/ajustar-moedas`,
        { method: "POST", body: { tipo_ajuste: tipoAjuste, valor, motivo } }
      );

      if (!okAjuste) {
        mostrarMensagem(mensagem, respostaAjuste?.erro || "Erro ao ajustar moedas.", "erro");
        return;
      }

      carregarHistorico();
    });
  }
}

carregarHistorico();
