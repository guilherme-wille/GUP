from flask import Blueprint, jsonify, session, request
from services.usuario.crianca.relatorio_desempenho_service import RelatorioDesempenhoService
from utils import familia_required
from services.conta_familia.listar_criancas_service import ListarCriancasService

relatorio_bp = Blueprint('relatorio', __name__, url_prefix='/relatorio')


@relatorio_bp.get('/')
@familia_required
def relatorio():
    if session.get('tipo_usuario') != 'responsavel':
        return jsonify({"erro": "Apenas responsáveis podem ver relatórios."}), 403

    conta_id = session.get('conta_id')
    criancas = ListarCriancasService.por_conta(conta_id)

    if not criancas:
        return jsonify({"erro": "Nenhuma criança cadastrada nesta família."}), 404

    crianca_selecionada_id = request.args.get('crianca_id')
    crianca_id = int(crianca_selecionada_id) if crianca_selecionada_id else criancas[0]["id"]

    try:
        dados_relatorio = RelatorioDesempenhoService.gerar(crianca_id, conta_id)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    # O service devolve objetos de Model (Crianca/Tarefa) dentro do dicionário;
    # aqui serializamos para JSON antes de responder.
    dados_relatorio = {
        **dados_relatorio,
        "crianca": dados_relatorio["crianca"].to_dict(),
        "tarefas_concluidas": [t.to_dict() for t in dados_relatorio["tarefas_concluidas"]],
    }

    return jsonify({
        "relatorio": dados_relatorio,
        "criancas": criancas,
    }), 200
