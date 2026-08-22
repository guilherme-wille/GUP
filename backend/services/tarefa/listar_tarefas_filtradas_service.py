from repositories.tarefa_repository import TarefaRepository


class ListarTarefasPorCriancaService:

    @staticmethod
    def executar(crianca_id, status=None):
        tarefas = TarefaRepository.listar_por_crianca(crianca_id, status)
        return [t.to_dict() for t in tarefas]


class ListarTarefasPorResponsavelService:

    @staticmethod
    def executar(responsavel_id, status=None):
        tarefas = TarefaRepository.listar_por_responsavel(responsavel_id, status)
        return [t.to_dict() for t in tarefas]