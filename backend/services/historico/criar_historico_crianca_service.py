from datetime import datetime
from models.historico_moeda_model import HistoricoMoeda


class HistoricoCriancaService:
    """Centraliza toda movimentação de moedas da criança (crédito/débito) e o registro no histórico."""

    @staticmethod
    def registrar_ganho_tarefa(crianca, tarefa):
        valor = tarefa.moedas_ganha

        crianca.moedas += valor
        crianca.atualizar(moedas=crianca.moedas)

        HistoricoCriancaService._criar_registro(
            crianca_id=crianca.id,
            origem="tarefa",
            valor=valor,  # positivo: entrada
            descricao=f"Tarefa concluída: {tarefa.titulo}",
        )
        return crianca

    @staticmethod
    def registrar_compra_recompensa(crianca, recompensa):
        HistoricoCriancaService._criar_registro(
            crianca_id=crianca.id,
            origem="recompensa",
            valor=-recompensa.custo_moedas,  # negativo: saída
            descricao=f"Resgatou: {recompensa.nome}",
        )

    @staticmethod
    def _criar_registro(crianca_id, origem, valor, descricao):
        historico = HistoricoMoeda(
            crianca_id=crianca_id,
            origem=origem,
            valor=valor,
            descricao=descricao,
            data_hora=datetime.now(),
        )
        historico.salvar()