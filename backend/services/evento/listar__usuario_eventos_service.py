from models.evento_model import EventoCalendario


class ListarEventoService:

    @staticmethod
    def executar(usuario_id):
        
        return EventoCalendario.query.filter_by(usuario_id=usuario_id).all()