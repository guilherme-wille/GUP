from flask import Blueprint, jsonify, session
from services.tarefa.listar_tarefas_filtradas_service import (
    ListarTarefasPorCriancaService,
    ListarTarefasPorResponsavelService,
)
from models.usuario_model import Usuario
from services.evento.listar__usuario_eventos_service import ListarEventoService
from utils import login_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.get('/dashboard')
@login_required
def index():
    usuario_id = session.get("usuario_id")

    usuario = Usuario.buscar_por_id(usuario_id)
    if not usuario:
        session.clear()
        return jsonify({"erro": "Usuário não encontrado. Faça login novamente."}), 401

    tem_familia = usuario.conta_id
    session["tem_familia"] = bool(tem_familia)

    if not tem_familia:
        # Antes: render_template('lobby.html')
        return jsonify({
            "tem_familia": False,
            "mensagem": "Você ainda não faz parte de uma família.",
        }), 200

    tipo_usuario = session.get('tipo_usuario')
    eventos = ListarEventoService.executar(usuario_id)
    eventos = [evento.to_dict() for evento in eventos]

    if tipo_usuario == 'responsavel':
        tarefas = ListarTarefasPorResponsavelService.executar(usuario_id)
        return jsonify({
            "tem_familia": True,
            "tipo_usuario": "responsavel",
            "tarefas": tarefas,
            "eventos": eventos,
        }), 200

    tarefas = ListarTarefasPorCriancaService.executar(usuario_id)
    return jsonify({
        "tem_familia": True,
        "tipo_usuario": "crianca",
        "tarefas": tarefas,
        "eventos": eventos,
    }), 200
