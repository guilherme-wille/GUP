from models.usuario_model import Usuario
from models.crianca_model import Crianca
from models.responsavel_model import Responsavel
from datetime import date, datetime
from werkzeug.security import generate_password_hash


IDADE_MINIMA_RESPONSAVEL = 18


class CriarUsuarioService:

    @staticmethod
    def calcular_idade(data_nasc: date) -> int:
        hoje = date.today()
        idade = hoje.year - data_nasc.year
        fez_aniversario = (hoje.month, hoje.day) >= (data_nasc.month, data_nasc.day)
        if not fez_aniversario:
            idade -= 1
        return idade
    

    @staticmethod
    def registrar_usuario(dados: dict):
        campos_obrigatorios = ["nome", "email", "senha", "data_nasc"]
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        if Usuario.query.filter_by(email=dados["email"]).first():
            raise ValueError("Já existe um usuário com esse email.")

        data_nasc = dados["data_nasc"]
        if isinstance(data_nasc, str):
            data_nasc = datetime.strptime(data_nasc, "%Y-%m-%d").date()

        idade = CriarUsuarioService.calcular_idade(data_nasc)
        senha_hash = generate_password_hash(dados["senha"])

        if idade >= IDADE_MINIMA_RESPONSAVEL:

            usuario = Responsavel(
                nome=dados["nome"],
                email=dados["email"],
                senha=senha_hash,
                data_nasc=data_nasc,
                tipo_usuario="responsavel"
            )
        else:
            usuario = Crianca(
                nome=dados["nome"],
                email=dados["email"],
                senha=senha_hash,
                data_nasc=data_nasc,
                tipo_usuario="crianca"
            )

        usuario.salvar()
        return usuario.to_dict()
