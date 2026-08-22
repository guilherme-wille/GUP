from models.evento_model import EventoCalendario
from datetime import datetime


class CriarEventoService:

    @staticmethod
    def registrar_evento(dados):
        campos_obrigatorios = ["titulo", "data", "usuario_id"]

        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        try:
            data_convertida = datetime.strptime(dados["data"], '%Y-%m-%d')
        except ValueError:
            raise ValueError("O formato da data é inválido.")

        evento = EventoCalendario(
            titulo=dados["titulo"],
            data=data_convertida,
            usuario_id=dados["usuario_id"]
        )

        evento.salvar()
        return evento.to_dict()