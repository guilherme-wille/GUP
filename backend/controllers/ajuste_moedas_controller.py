from flask import Blueprint, jsonify, request, session
from services.historico.alterar_moedas_service import AjustarMoedasService
from utils import familia_required

ajuste_moedas_bp = Blueprint('ajuste_moedas', __name__, url_prefix='/criancas')


@ajuste_moedas_bp.post('/<int:crianca_id>/ajustar-moedas')
@familia_required
def ajustar_moedas(crianca_id):
    if session.get('tipo_usuario') != 'responsavel':
        return jsonify({"erro": "Apenas responsáveis podem ajustar moedas."}), 403

    dados = request.get_json() or {}
    tipo_ajuste = dados.get('tipo_ajuste')  # 'adicionar' ou 'remover'
    valor = dados.get('valor')
    motivo = dados.get('motivo')

    try:
        valor_int = abs(int(valor))
        if tipo_ajuste == 'remover':
            valor_int = -valor_int

        crianca = AjustarMoedasService.executar(
            conta_id=session.get('conta_id'),
            crianca_id=crianca_id,
            valor=valor_int,
            motivo=motivo,
        )
        return jsonify(crianca.to_dict()), 200

    except (ValueError, TypeError) as e:
        return jsonify({"erro": str(e)}), 400
