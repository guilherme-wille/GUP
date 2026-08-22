from datetime import datetime
from models.crianca_model import Crianca
from models.historico_moeda_model import HistoricoMoeda


class AjustarMoedasService:

    @staticmethod
    def executar(conta_id, crianca_id, valor, motivo):
        crianca = Crianca.buscar_por_id(crianca_id)
        if not crianca:
            raise ValueError("Criança não encontrada.")

        if crianca.conta_id != conta_id:
            raise ValueError("Essa criança não pertence à sua família.")

        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("O valor deve ser um número inteiro.")

        if valor == 0:
            raise ValueError("Informe um valor diferente de zero.")

        if not motivo or not motivo.strip():
            raise ValueError("Informe o motivo do ajuste.")

        novo_saldo = crianca.moedas + valor
        if novo_saldo < 0:
            raise ValueError("Esse ajuste deixaria o saldo da criança negativo.")

        crianca.atualizar(moedas=novo_saldo)

        historico = HistoricoMoeda(
            crianca_id=crianca.id,
            origem="ajuste_manual",
            valor=valor,  # positivo: crédito | negativo: débito
            descricao=motivo.strip(),
            data_hora=datetime.now(),
        )
        historico.salvar()

        return crianca