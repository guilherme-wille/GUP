from . import db
from .base_model import ModeloBase

class Resgate(ModeloBase):
    # registro de recompensa cada crianca resgato e quando !!!tabela nova!!! para a tela de premios
    __tablename__ = 'resgate'

    data_resgate = db.Column(db.DateTime, nullable=False)
    crianca_id = db.Column(db.Integer, db.ForeignKey('crianca.id'), nullable=False)
    recompensa_id = db.Column(db.Integer, db.ForeignKey('recompensa.id'), nullable=False)

    crianca = db.relationship('Crianca', backref='resgates', lazy=True)
    recompensa = db.relationship('Recompensa', backref='resgates', lazy=True)