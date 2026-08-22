from . import db
from .base_model import ModeloBase

class HistoricoMoeda(ModeloBase):
    __tablename__ = 'historico_moeda'

    origem = db.Column(db.String(20), nullable=False)     
    descricao = db.Column(db.String(255), nullable=True)  
    data_hora = db.Column(db.DateTime, nullable=False)
    valor = db.Column(db.Integer, nullable=False)          

    crianca_id = db.Column(db.Integer, db.ForeignKey('crianca.id'), nullable=False)