from models.crianca_model import Crianca
from models.recompensa_model import Recompensa
from services.historico.criar_historico_crianca_service import HistoricoCriancaService


class ComprarRecompensaService:

    @staticmethod
    def executar(usuario_id, recompensa_id):
        crianca = Crianca.buscar_por_id(usuario_id)
        if not crianca:
            raise ValueError("Criança não encontrada.")

        recompensa = Recompensa.query.get(recompensa_id)
        if not recompensa:
            raise ValueError("Recompensa não encontrada.")

        if recompensa.status != "Disponivel":
            raise ValueError("Essa recompensa não está mais disponível.")

        if crianca.moedas < recompensa.custo_moedas:
            raise ValueError("Moedas insuficientes.")

        novo_saldo = crianca.moedas - recompensa.custo_moedas
        crianca.atualizar(moedas=novo_saldo)

        # registra a saída no histórico
        HistoricoCriancaService.registrar_compra_recompensa(crianca, recompensa)

        return crianca.to_dict()