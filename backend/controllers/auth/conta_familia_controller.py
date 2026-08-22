from flask import Blueprint, jsonify, request, session
from sqlalchemy.exc import SQLAlchemyError
from services.conta_familia.criar_conta_familia_service import CriarContaFamiliaService
from models.conta_familia_model import ContaFamilia
from models.usuario_model import Usuario
from services.conta_familia.login_service import LoginService
from services.conta_familia.listar_membros_service import ListarMembrosFamiliaService
from utils import login_required
from models import db

conta_bp = Blueprint("conta_familia", __name__, url_prefix="/contas")


@conta_bp.post('/criar')
@login_required
def criar_conta():
    try:
        dados = request.get_json() or {}

        id_usuario_logado = session.get('usuario_id')
        usuario = Usuario.buscar_por_id(id_usuario_logado)

        dados['email_dono'] = usuario.email

        conta = CriarContaFamiliaService.registrar_conta(dados)

        usuario.atualizar(conta_id=conta["id"])
        session['tem_familia'] = True
        session['conta_id'] = conta["id"]

        return jsonify(conta), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar a conta família no banco de dados."}), 500


@conta_bp.post('/login')
@login_required
def login():
    try:
        dados = request.get_json() or {}
        conta = LoginService.autenticar(dados.get("email_dono"), dados.get("pin"))

        id_usuario_logado = session.get('usuario_id')
        usuario = Usuario.buscar_por_id(id_usuario_logado)

        usuario.atualizar(conta_id=conta["id"])
        session['tem_familia'] = True
        session['conta_id'] = conta["id"]

        return jsonify(conta), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@conta_bp.get('/info')
@login_required
def informacoes_conta():
    conta_id = session.get("conta_id")

    if not conta_id:
        return jsonify({"erro": "Você ainda não faz parte de uma família."}), 404

    membros = ListarMembrosFamiliaService.listar(conta_id)

    conta = ContaFamilia.query.get(conta_id)
    if not conta:
        return jsonify({"erro": "Conta não encontrada no banco de dados."}), 404

    return jsonify({
        "nome_familia": conta.nome,
        "membros": membros,
    }), 200
