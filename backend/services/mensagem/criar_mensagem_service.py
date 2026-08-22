from models.tarefa_model import Tarefa
from models.mensagem_tarefa_model import MensagemTarefa


class CriarMensagemTarefaService:

    @staticmethod
    def executar(tarefa_id, dados):
        tarefa = Tarefa.buscar_por_id(tarefa_id)

        if tarefa is None:
            raise ValueError("Não foi possível encontrar a tarefa")

        autor_tipo = dados.get("autor_tipo")
        mensagem_texto = dados.get("mensagem")

        if autor_tipo not in ("filho", "responsavel"):
            raise ValueError("O campo 'autor_tipo' deve ser 'filho' ou 'responsavel'")

        if not mensagem_texto:
            raise ValueError("O campo 'mensagem' é obrigatório")

        mensagem = MensagemTarefa(
            tarefa_id=tarefa_id,
            autor_tipo=autor_tipo,
            mensagem=mensagem_texto,
        )

        mensagem.salvar()
        return mensagem.to_dict()