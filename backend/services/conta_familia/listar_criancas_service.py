# services/usuario/listar_criancas_service.py
from models.crianca_model import Crianca

class ListarCriancasService:
    @staticmethod
    def por_conta(conta_id):
        # Busca todas as crianças que pertencem à conta da família logada
        criancas = Crianca.query.filter_by(conta_id=conta_id).all()
        
        # Se sua classe Crianca não tiver o .to_dict() pronto, retorne os objetos:
        # return criancas 
        return [crianca.to_dict() for crianca in criancas]