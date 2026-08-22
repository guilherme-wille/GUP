from models.crianca_model import Crianca
from models.recompensa_model import Recompensa


class DefinirMetaService:

    @staticmethod
    def executar(usuario_id, recompensa_id):
        crianca = Crianca.buscar_por_id(usuario_id)
        if not crianca:
            raise ValueError("Criança não encontrada.")

        recompensa = Recompensa.query.get(recompensa_id)
        if not recompensa:
            raise ValueError("Recompensa não encontrada.")

        crianca.atualizar(meta_id=recompensa.id)
        return crianca