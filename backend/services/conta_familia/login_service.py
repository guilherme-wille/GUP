from werkzeug.security import check_password_hash
from models.conta_familia_model import ContaFamilia


class LoginService:
    @staticmethod
    def autenticar(email_dono: str, pin: str):
        if not email_dono or not pin:
            raise ValueError("Email e pin são obrigatórios.")

        conta_familia = ContaFamilia.query.filter_by(email_dono=email_dono).first()

        if conta_familia is None:
            raise ValueError("Email ou pin inválidos.")

        if not check_password_hash(conta_familia.pin, pin):
            raise ValueError("Email ou pin inválidos.")

        return conta_familia.to_dict()