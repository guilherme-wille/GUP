from models.usuario_model import Usuario


class DeletarUsuarioService:

    @staticmethod
    def executar(usuario_id):
        usuario = Usuario.buscar_por_id(usuario_id)

        if usuario is None:
            raise ValueError("Usuario não pode ser deletado")

        usuario.deletar()
        return True