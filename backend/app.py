import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from controllers import all_blueprints


def criar_app():
    pasta = os.path.abspath(os.path.dirname(__file__))

    # Sem template_folder/static_folder de Jinja: o frontend agora é uma
    # aplicação separada (HTML + CSS + JS puro) que consome esta API via fetch.
    # Mantemos apenas a pasta "static" para servir os arquivos de comprovação
    # de tarefas (uploads de imagem), que continuam sendo simples arquivos.
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "gup.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "123456"

    # Cookie de sessão: como o frontend roda em outra origem (outra porta),
    # o cookie precisa poder ser enviado em requisições cross-origin feitas
    # com fetch(..., { credentials: "include" }).
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False

    # Libera o CORS para que o frontend (ex.: http://127.0.0.1:5500) possa
    # chamar esta API e enviar/receber o cookie de sessão.
    CORS(
        app,
        supports_credentials=True,
        origins=[
            "http://127.0.0.1:5500",
            "http://localhost:5500",
            "http://127.0.0.1:5501",
            "http://localhost:5501",
        ],
    )

    db.init_app(app)

    @app.errorhandler(413)
    def arquivo_muito_grande(e):
        return jsonify({"erro": "O arquivo enviado excede o limite de 5MB."}), 413

    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    @app.get("/")
    def home():
        return jsonify({
            "mensagem": "API do GUP (Flask + SQLAlchemy) funcionando.",
            "rotas": {
                "cadastro": "POST /usuarios/cadastro",
                "login_usuario": "POST /usuarios/login",
                "logout": "POST /usuarios/logout",
                "usuario_logado": "GET /usuarios/me",
                "criar_conta_familia": "POST /contas/criar",
                "login_conta_familia": "POST /contas/login",
                "info_conta_familia": "GET /contas/info",
                "dashboard": "GET /dashboard",
                "criar_tarefa_info": "GET /tarefas/criar-info",
                "criar_tarefa": "POST /tarefas/criar",
                "atualizar_status_tarefa": "POST /tarefas/<id>/status",
                "criar_evento": "POST /eventos",
                "historico": "GET /historico",
                "ajustar_moedas": "POST /criancas/<id>/ajustar-moedas",
                "recompensas": "GET|POST /recompensas",
                "comprar_recompensa": "POST /recompensas/comprar/<id>",
                "definir_meta": "POST /recompensas/meta/<id>",
                "relatorio": "GET /relatorio",
            }
        })

    with app.app_context():
        db.create_all()

    return app


app = criar_app()

if __name__ == '__main__':
    app.run(debug=True)
