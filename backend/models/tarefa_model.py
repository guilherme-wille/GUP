from . import db
from .base_model import ModeloBase

class Tarefa(ModeloBase):
    __tablename__ = 'tarefa'

    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, default=None, nullable=True)
    status = db.Column(db.String(30), nullable=False, default='pendente')
    horario_limite = db.Column(db.DateTime, nullable=False)
    data_conclusao = db.Column(db.DateTime, nullable=True)

    moedas_ganha = db.Column(db.Integer, nullable=False, default=0)
    moedas_perda = db.Column(db.Integer, nullable=False, default=0)
    moedas_atraso = db.Column(db.Integer, nullable=False, default=0)
    xp_ganho = db.Column(db.Integer, nullable=False, default=0)
    foto_comprovacao = db.Column(db.String(255), default=None)
    tipo_comprovacao = db.Column(db.String(20), default=None, nullable=True)

    crianca_id = db.Column(db.Integer, db.ForeignKey('crianca.id'), nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('responsavel.id'), nullable=False)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta_familia.id'))

    mensagens = db.relationship('MensagemTarefa', backref='tarefa', lazy=True)