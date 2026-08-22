from . import db
from .base_model import ModeloBase

class MensagemTarefa(ModeloBase):
    __tablename__ = 'mensagem_tarefa'

    texto = db.Column(db.Text, nullable=False)
    remetente = db.Column(db.String(30), nullable=False)
    destinatario = db.Column(db.String(30), nullable=False)

    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefa.id'), nullable=False)