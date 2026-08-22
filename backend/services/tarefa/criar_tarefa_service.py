from models.tarefa_model import Tarefa
from datetime import datetime


class CriarTarefaService:

    @staticmethod
    def criar_tarefa(dados):
        campos_obrigatorios = ["titulo", "horario_limite",
                               "crianca_id", "responsavel_id"]

        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        horario_limite = dados["horario_limite"]
        if isinstance(horario_limite, str):
            # input[type=datetime-local] envia "AAAA-MM-DDTHH:MM"
            horario_limite = datetime.strptime(horario_limite, "%Y-%m-%dT%H:%M")

        tarefa = Tarefa(
            titulo=dados["titulo"],
            descricao=dados.get("descricao"),
            status=dados.get("status") or "pendente",
            horario_limite=horario_limite,
            crianca_id=dados["crianca_id"],
            responsavel_id=dados["responsavel_id"],
            conta_id=dados.get("conta_id"),
            xp_ganho=int(dados.get("xp_ganho") or 0),
            moedas_ganha=int(dados.get("moedas_ganha") or 0),
            moedas_perda=int(dados.get("moedas_perda") or 0),
            moedas_atraso=int(dados.get("moedas_atraso") or 0),
        )

        tarefa.salvar()
        return tarefa.to_dict()