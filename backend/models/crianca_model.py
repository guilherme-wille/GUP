from . import db
from .usuario_model import Usuario

class Crianca(Usuario):
    __tablename__ = 'crianca'

    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)

    moedas = db.Column(db.Integer, nullable=False, default=0)
    xp = db.Column(db.Integer, nullable=False, default=0)
    strike_atual = db.Column(db.Integer, nullable=False, default=0)
    nivel = db.Column(db.Integer, nullable=False, default=0)

    cor_girafa = db.Column(db.String(15), default='amarelo')
    bolinha_girafa = db.Column(db.String(15), default='marrom')

    tarefas = db.relationship('Tarefa', backref='crianca', lazy=True)
    historico = db.relationship('HistoricoMoeda', backref='crianca', lazy=True)
    meta_id = db.Column(db.Integer, db.ForeignKey('recompensa.id'), nullable=True)
    meta = db.relationship('Recompensa')

    __mapper_args__ = {
        'polymorphic_identity': 'crianca',
    }