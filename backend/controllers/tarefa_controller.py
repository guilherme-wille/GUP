import os
import uuid
from flask import Blueprint, jsonify, request, session, current_app
from services.tarefa.criar_tarefa_service import CriarTarefaService
from services.tarefa.atualizar_status_service import AtualizarStatusTarefaService
from services.conta_familia.listar_criancas_service import ListarCriancasService
from utils import familia_required

tarefa_bp = Blueprint('tarefas', __name__, url_prefix='/tarefas')

EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
PASTA_UPLOAD = os.path.join('uploads', 'comprovacoes')  # dentro de /static


def _extensao_valida(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS


@tarefa_bp.get('/criar-info')
@familia_required
def criar_tarefa_info():
    """Antes era a versão GET de /tarefas/criar, que renderizava o
    formulário com a lista de crianças. Agora o frontend busca essa
    lista via fetch para popular o <select> antes de enviar o POST."""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 'responsavel':
        return jsonify({"erro": "Apenas responsáveis podem criar tarefas."}), 403

    conta_id = session.get("conta_id")
    criancas = ListarCriancasService.por_conta(conta_id)
    return jsonify({"criancas": criancas}), 200


@tarefa_bp.post('/criar')
@familia_required
def criar_tarefa():
    if 'usuario_id' not in session or session.get('tipo_usuario') != 'responsavel':
        return jsonify({"erro": "Apenas responsáveis podem criar tarefas."}), 403

    conta_id = session.get("conta_id")
    criancas = ListarCriancasService.por_conta(conta_id)

    dados = request.get_json() or {}
    if not dados:
        return jsonify({"erro": "Envie os dados da tarefa."}), 400

    dados["responsavel_id"] = session["usuario_id"]
    dados["conta_id"] = conta_id

    try:
        ids_validos = {c["id"] for c in criancas}
        crianca_id = int(dados.get("crianca_id") or 0)

        if crianca_id not in ids_validos:
            raise ValueError("Selecione uma criança válida da sua família.")

        tarefa = CriarTarefaService.criar_tarefa(dados)
        return jsonify(tarefa), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@tarefa_bp.post('/<int:id>/status')
@familia_required
def atualizar_status(id):
    if 'usuario_id' not in session:
        return jsonify({"erro": "Você precisa estar logado."}), 401

    # Continua multipart/form-data pois envolve upload de arquivo.
    novo_status = request.form.get("novo_status")
    arquivo = request.files.get("foto_comprovacao")

    caminho_foto = None
    tipo_comprovacao = None

    if arquivo and arquivo.filename:
        if not _extensao_valida(arquivo.filename):
            return jsonify({
                "erro": "O arquivo precisa ser uma imagem (png, jpg, jpeg, gif ou webp)."
            }), 400

        pasta_absoluta = os.path.join(current_app.root_path, 'static', PASTA_UPLOAD)
        os.makedirs(pasta_absoluta, exist_ok=True)

        extensao = arquivo.filename.rsplit('.', 1)[1].lower()
        nome_arquivo = f"{uuid.uuid4().hex}.{extensao}"
        arquivo.save(os.path.join(pasta_absoluta, nome_arquivo))

        caminho_foto = f"{PASTA_UPLOAD}/{nome_arquivo}".replace(os.sep, '/')
        tipo_comprovacao = "imagem"

    try:
        tarefa = AtualizarStatusTarefaService.executar(
            id,
            novo_status,
            session["usuario_id"],
            session.get("tipo_usuario"),
            foto_comprovacao=caminho_foto,
            tipo_comprovacao=tipo_comprovacao,
        )
        return jsonify(tarefa), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
