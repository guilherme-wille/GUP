from controllers.auth.conta_familia_controller import conta_bp
from controllers.auth.usuario_controller import usuario_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.recompensa_controller import recompensa_bp
from controllers.tarefa_controller import tarefa_bp
from controllers.historico_controller import historico_bp
from controllers.evento_controller import evento_bp
from controllers.ajuste_moedas_controller import ajuste_moedas_bp
from controllers.relatorio_controller import relatorio_bp

all_blueprints = [usuario_bp, dashboard_bp,
                  conta_bp, tarefa_bp, recompensa_bp,
                  historico_bp, evento_bp,
                  ajuste_moedas_bp, relatorio_bp]
