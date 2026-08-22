from models.tarefa_model import Tarefa


class TarefaRepository:
    """Acesso a dados da Tarefa."""

    @staticmethod
    def buscar_por_id(tarefa_id):
        return Tarefa.buscar_por_id(tarefa_id)

    @staticmethod
    def atualizar_status(tarefa, novo_status, foto_comprovacao=None, tipo_comprovacao=None, data_conclusao=None):
        dados = {"status": novo_status}
        if foto_comprovacao is not None:
            dados["foto_comprovacao"] = foto_comprovacao
        if tipo_comprovacao is not None:
            dados["tipo_comprovacao"] = tipo_comprovacao
        if data_conclusao is not None:
            dados["data_conclusao"] = data_conclusao

        tarefa.atualizar(**dados)
        return tarefa

    @staticmethod
    def listar_por_crianca(crianca_id, status=None):
        consulta = Tarefa.query.filter(Tarefa.crianca_id == crianca_id)

        if status:
            consulta = consulta.filter(Tarefa.status == status)

        return consulta.order_by(Tarefa.horario_limite.asc()).all()

    @staticmethod
    def listar_por_responsavel(responsavel_id, status=None):
        consulta = Tarefa.query.filter(Tarefa.responsavel_id == responsavel_id)

        if status:
            consulta = consulta.filter(Tarefa.status == status)

        return consulta.order_by(Tarefa.horario_limite.asc()).all()