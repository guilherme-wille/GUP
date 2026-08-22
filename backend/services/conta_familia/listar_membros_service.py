from models.usuario_model import Usuario

class ListarMembrosFamiliaService:

    @staticmethod
    def listar(conta_id):
        # Busca todas as crianças que pertencem à conta da família logada
        usuarios = Usuario.query.filter_by(conta_id=conta_id).all()
        
        # Se sua classe Crianca não tiver o .to_dict() pronto, retorne os objetos:
        # return criancas 
        return [usuario.to_dict() for usuario in usuarios]