from models.recompensa_model import Recompensa


class CriarRecompensaService:

    @staticmethod
    def registrar_recompensa(dados):
        campos_obrigatorios = ["nome", "custo_moedas"]
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        try:
            custo_moedas = int(dados["custo_moedas"])
        except (TypeError, ValueError):
            raise ValueError("Custo em moedas deve ser um número.")

        if custo_moedas <= 0:
            raise ValueError("Custo em moedas deve ser maior que zero.")

        recompensa = Recompensa(
            nome=dados["nome"],
            custo_moedas=custo_moedas,
            status=dados.get("status", "Disponivel"),
        )
        recompensa.salvar()
        return recompensa.to_dict()