from models.resgate_model import Resgate


class ListarResgateService:
    def executar(self):
        return Resgate.query.all()