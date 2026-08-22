from models.resgate_model import Resgate


class CriarResgateService:
    def executar(self, dados):
        campos_obrigatorios = ["crianca_id", "recompensa_id"]

        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        resgate = Resgate(
            crianca_id=dados["crianca_id"],
            recompensa_id=dados["recompensa_id"],
        )

        resgate.salvar()
        return resgate.to_dict()