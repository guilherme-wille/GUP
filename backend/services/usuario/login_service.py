from werkzeug.security import check_password_hash
from models.usuario_model import Usuario


class LoginService:
    @staticmethod
    def autenticar(email: str, senha: str):
        if not email or not senha:
            raise ValueError("Email e senha são obrigatórios.")

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario is None:
            raise ValueError("Email ou senha inválidos.")

        if not check_password_hash(usuario.senha, senha):
            raise ValueError("Email ou senha inválidos.")

        return usuario.to_dict()