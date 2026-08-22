from models.tarefa_model import Tarefa


class AtualizarStatusRepository:
    """Camada de acesso a dados para atualização de status de tarefa."""

    @staticmethod
    def buscar_tarefa_por_id(tarefa_id):
        return Tarefa.buscar_por_id(tarefa_id)

    @staticmethod
    def salvar_novo_status(tarefa, novo_status):
        tarefa.atualizar(status=novo_status)
        return tarefa