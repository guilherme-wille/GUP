from flask import Blueprint, jsonify, session, request
from models.crianca_model import Crianca
from models.historico_moeda_model import HistoricoMoeda
from utils import familia_required
from services.conta_familia.listar_criancas_service import ListarCriancasService

historico_bp = Blueprint('historico', __name__)


@historico_bp.get('/historico')
@familia_required
def historico():
    eh_responsavel = session.get('tipo_usuario') == 'responsavel'
    conta_id = session.get('conta_id')
    usuario_id = session.get('usuario_id')

    if eh_responsavel:
        criancas = ListarCriancasService.por_conta(conta_id)
        if not criancas:
            return jsonify({"erro": "Nenhuma criança cadastrada nesta família."}), 404

        crianca_selecionada_id = request.args.get('crianca_id')
        if crianca_selecionada_id:
            crianca_obj = Crianca.buscar_por_id(crianca_selecionada_id)
            crianca = crianca_obj.to_dict() if crianca_obj else None
        else:
            crianca = criancas[0] if criancas else None
    else:
        criancas = []
        crianca_obj = Crianca.buscar_por_id(usuario_id)
        crianca = crianca_obj.to_dict() if crianca_obj else None

    lista_historico = []
    if crianca:
        registros = (
            HistoricoMoeda.query
            .filter_by(crianca_id=crianca["id"])
            .order_by(HistoricoMoeda.id.desc())
            .all()
        )
        lista_historico = [registro.to_dict() for registro in registros]

    return jsonify({
        "crianca": crianca,
        "criancas": criancas,
        "historico": lista_historico,
        "eh_responsavel": eh_responsavel,
    }), 200
