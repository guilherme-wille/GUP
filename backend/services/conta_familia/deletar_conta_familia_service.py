from models.conta_familia_model import ContaFamilia


class DeletarContaFamiliaService:
    def deletar_conta(self, conta_familia_id):
        conta_familia = ContaFamilia.buscar_por_id(conta_familia_id)

        if conta_familia is None:
            raise ValueError("Conta família não pode ser deletada")

        conta_familia.deletar()
        return True