from datetime import datetime
from repositories.tarefa_repository import TarefaRepository
from models.crianca_model import Crianca
from models.historico_moeda_model import HistoricoMoeda

STATUS_VALIDOS = {"pendente", "espera", "concluida"}


class AtualizarStatusTarefaService:

    @staticmethod
    def executar(tarefa_id, novo_status, usuario_id, tipo_usuario, foto_comprovacao=None, tipo_comprovacao=None):
        tarefa = TarefaRepository.buscar_por_id(tarefa_id)

        if tarefa is None:
            raise ValueError("Não foi possível encontrar a tarefa")

        if tarefa.status == "concluida":
            raise ValueError("Esta tarefa já foi concluída e as moedas já foram pagas.")

        novo_status = (novo_status or "").lower()
        if novo_status not in STATUS_VALIDOS:
            raise ValueError("Status inválido")

        if tipo_usuario == "crianca":
            if tarefa.crianca_id != usuario_id:
                raise ValueError("Essa tarefa não é sua")
            if novo_status != "espera":
                raise ValueError("A criança só pode enviar a tarefa para análise")
            if not foto_comprovacao:
                raise ValueError("Envie uma foto como comprovação para concluir a tarefa.")

        elif tipo_usuario == "responsavel":
            if tarefa.responsavel_id != usuario_id:
                raise ValueError("Essa tarefa não é da sua família")
            if novo_status not in ("concluida", "pendente"):
                raise ValueError("O responsável só pode aprovar ou recusar a tarefa")

        else:
            raise ValueError("Tipo de usuário inválido")

        data_conclusao = None
        if novo_status == "concluida":
            data_conclusao = datetime.now()
            AtualizarStatusTarefaService._pagar_recompensa(tarefa)

        tarefa = TarefaRepository.atualizar_status(
            tarefa,
            novo_status,
            foto_comprovacao=foto_comprovacao,
            tipo_comprovacao=tipo_comprovacao,
            data_conclusao=data_conclusao,
        )
        return tarefa.to_dict()

    @staticmethod
    def _pagar_recompensa(tarefa):
        crianca = Crianca.buscar_por_id(tarefa.crianca_id)
        if not crianca:
            raise ValueError("Criança não encontrada para receber a recompensa.")

        valor = tarefa.moedas_ganha
        crianca.moedas += valor
        crianca.atualizar(moedas=crianca.moedas)

        historico = HistoricoMoeda(
            crianca_id=crianca.id,
            origem="tarefa",
            valor=valor,
            descricao=f"Tarefa concluída: {tarefa.titulo}",
            data_hora=datetime.now(),
        )
        historico.salvar()