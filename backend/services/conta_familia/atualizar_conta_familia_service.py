from models.conta_familia_model import ContaFamilia


class AtualizarContaFamiliaService:
    def atualizar_conta(self, conta_familia_id, dados):
        conta_familia = ContaFamilia.buscar_por_id(conta_familia_id)

        if conta_familia is None:
            raise ValueError("Não foi possível encontrar a conta família")

        conta_familia.atualizar(
            pin=dados.get("pin"),
            nome=dados.get("nome"),
        )

        return conta_familia.to_dict()