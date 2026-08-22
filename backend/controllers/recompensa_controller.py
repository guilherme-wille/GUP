from flask import Blueprint, request, jsonify, session
from models.crianca_model import Crianca
from models.recompensa_model import Recompensa
from services.recompensa.criar_recompensa_service import CriarRecompensaService
from services.recompensa.comprar_recompensa_service import ComprarRecompensaService
from services.recompensa.definir_meta_service import DefinirMetaService
from utils import familia_required

recompensa_bp = Blueprint("recompensas", __name__, url_prefix="/recompensas")


@recompensa_bp.get('/')
@familia_required
def listar():
    recompensas = [r.to_dict() for r in Recompensa.query.all()]

    crianca_logada = None
    if session.get('tipo_usuario') == 'crianca':
        crianca = Crianca.buscar_por_id(session.get('usuario_id'))
        crianca_logada = crianca.to_dict() if crianca else None

    return jsonify({
        "recompensas": recompensas,
        "crianca_logada": crianca_logada,
        "tipo_usuario": session.get('tipo_usuario'),
    }), 200


@recompensa_bp.post('/')
@familia_required
def criar():
    if session.get('tipo_usuario') != 'responsavel':
        return jsonify({"erro": "Apenas responsáveis podem criar recompensas."}), 403

    dados = request.get_json() or {}

    try:
        recompensa = CriarRecompensaService.registrar_recompensa(dados)
        return jsonify(recompensa), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@recompensa_bp.post('/comprar/<int:id>')
@familia_required
def comprar(id):
    if session.get('tipo_usuario') != 'crianca':
        return jsonify({"erro": "Apenas crianças podem comprar recompensas."}), 403

    try:
        crianca = ComprarRecompensaService.executar(session.get('usuario_id'), id)
        return jsonify(crianca), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@recompensa_bp.post('/meta/<int:id>')
@familia_required
def meta(id):
    if session.get('tipo_usuario') != 'crianca':
        return jsonify({"erro": "Apenas crianças podem definir metas."}), 403

    try:
        crianca = DefinirMetaService.executar(session.get('usuario_id'), id)
        session["meta"] = crianca.meta_id
        return jsonify(crianca.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
