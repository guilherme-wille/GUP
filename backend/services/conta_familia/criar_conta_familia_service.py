from models.conta_familia_model import ContaFamilia
from werkzeug.security import generate_password_hash

class CriarContaFamiliaService:

    @staticmethod
    def registrar_conta(dados):
        campos_obrigatorios = ["nome", "pin"]

        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        pin_hash = generate_password_hash(dados["pin"])

        conta_familia = ContaFamilia(
            nome=dados["nome"],
            pin=pin_hash,
            email_dono=dados["email_dono"]
        )

        conta_familia.salvar()
        return conta_familia.to_dict()