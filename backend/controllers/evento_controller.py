from flask import Blueprint, jsonify, request, session
from services.evento.criar_evento_service import CriarEventoService
from services.evento.listar__usuario_eventos_service import ListarEventoService
from utils import familia_required

evento_bp = Blueprint("eventos", __name__, url_prefix="/eventos")


@evento_bp.get('/')
@familia_required
def listar_eventos():
    """Antes o GET de /eventos apenas renderizava o formulário (evento.html).
    Agora devolve a lista de eventos do usuário logado, útil para o
    frontend exibir a agenda antes de criar um novo evento."""
    usuario_id = session.get("usuario_id")
    eventos = ListarEventoService.executar(usuario_id)
    return jsonify([evento.to_dict() for evento in eventos]), 200


@evento_bp.post('/')
@familia_required
def criar_evento():
    dados = request.get_json() or {}

    if not dados:
        return jsonify({"erro": "Envie os dados do evento."}), 400

    usuario_logado = session.get("usuario_id")
    conta_id = session.get("conta_id")

    dados["usuario_id"] = usuario_logado
    dados["conta_id"] = conta_id

    try:
        evento = CriarEventoService.registrar_evento(dados)
        return jsonify(evento), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
