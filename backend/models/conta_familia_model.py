from .base_model import ModeloBase
from . import db

class ContaFamilia(ModeloBase):
    __tablename__ = 'conta_familia'

    pin = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(30), nullable=False)
    email_dono = db.Column(db.String(150), nullable=False)
    
    responsaveis = db.relationship('Responsavel', backref='conta', lazy=True)
    criancas = db.relationship('Crianca', backref='conta', lazy=True)