from . import db
from .base_model import ModeloBase

class Recompensa(ModeloBase):
    __tablename__ = 'recompensa'

    nome = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    custo_moedas = db.Column(db.Integer, nullable=False)
