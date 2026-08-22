from models.tarefa_model import Tarefa
from models.crianca_model import Crianca


class RelatorioDesempenhoService:

    @staticmethod
    def gerar(crianca_id, conta_id=None):
        crianca = Crianca.buscar_por_id(crianca_id)
        if not crianca:
            raise ValueError("Criança não encontrada.")

        if conta_id is not None and crianca.conta_id != conta_id:
            raise ValueError("Essa criança não pertence à sua família.")

        tarefas = Tarefa.query.filter_by(crianca_id=crianca_id).all()

        concluidas = [t for t in tarefas if t.status == "concluida"]
        pendentes = [t for t in tarefas if t.status == "pendente"]
        em_espera = [t for t in tarefas if t.status == "espera"]

        total = len(tarefas)
        total_concluidas = len(concluidas)
        taxa_conclusao = round((total_concluidas / total) * 100, 1) if total > 0 else 0

        moedas_ganhas = sum(t.moedas_ganha for t in concluidas)
        xp_ganho = sum(t.xp_ganho for t in concluidas)

        return {
            "crianca": crianca,
            "total_tarefas": total,
            "total_concluidas": total_concluidas,
            "total_pendentes": len(pendentes),
            "total_em_espera": len(em_espera),
            "taxa_conclusao": taxa_conclusao,
            "moedas_ganhas": moedas_ganhas,
            "xp_ganho": xp_ganho,
            "tarefas_concluidas": sorted(concluidas, key=lambda t: t.data_conclusao or t.id, reverse=True),
        }