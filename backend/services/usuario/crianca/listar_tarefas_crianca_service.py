# services/tarefa/listar_tarefas_service.py
from models.tarefa_model import Tarefa

class ListarTarefasService:
    @staticmethod
    def por_crianca(crianca_id):
        # Traz todas as tarefas associadas àquela criança
        tarefas = Tarefa.query.filter_by(crianca_id=crianca_id).all()
        return [tarefa.to_dict() for tarefa in tarefas]
        
    @staticmethod
    def por_conta_familia(conta_id):
        # Traz todas as tarefas da família inteira para o responsável ver
        tarefas = Tarefa.query.filter_by(conta_id=conta_id).all()
        return [tarefa.to_dict() for tarefa in tarefas]