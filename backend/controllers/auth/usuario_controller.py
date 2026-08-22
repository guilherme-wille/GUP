from flask import Blueprint, jsonify, request, session
from sqlalchemy.exc import SQLAlchemyError
from services.usuario.criar_usuario_service import CriarUsuarioService
from services.usuario.login_service import LoginService
from models import db

usuario_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuario_bp.post('/cadastro')
def cadastro():
    try:
        dados = request.get_json() or {}
        usuario = CriarUsuarioService.registrar_usuario(dados)

        session['usuario_id'] = usuario["id"]
        session['nome_usuario'] = usuario["nome"]
        session['tipo_usuario'] = usuario["tipo_usuario"]
        session['tem_familia'] = usuario.get("conta_id") is not None
        session['conta_id'] = usuario.get("conta_id")

        return jsonify(usuario), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar usuário no banco de dados."}), 500


@usuario_bp.post('/login')
def login():
    try:
        dados = request.get_json() or {}
        usuario = LoginService.autenticar(dados.get("email"), dados.get("senha"))

        session['usuario_id'] = usuario["id"]
        session['nome_usuario'] = usuario["nome"]
        session['tipo_usuario'] = usuario["tipo_usuario"]
        session['tem_familia'] = usuario.get("conta_id") is not None
        session['conta_id'] = usuario.get("conta_id")

        return jsonify(usuario), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@usuario_bp.post('/logout')
def logout():
    session.clear()
    return jsonify({"mensagem": "Sessão encerrada com sucesso."}), 200


@usuario_bp.get('/me')
def me():
    """Substitui a checagem de sessão que antes era feita implicitamente
    dentro dos templates Jinja. O frontend usa essa rota para saber se
    existe um usuário logado e para onde deve navegar."""
    if 'usuario_id' not in session:
        return jsonify({"logado": False}), 200

    return jsonify({
        "logado": True,
        "usuario_id": session.get("usuario_id"),
        "nome_usuario": session.get("nome_usuario"),
        "tipo_usuario": session.get("tipo_usuario"),
        "tem_familia": bool(session.get("tem_familia")),
        "conta_id": session.get("conta_id"),
    }), 200
