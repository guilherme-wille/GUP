from . import db
from .base_model import ModeloBase

class EventoCalendario(ModeloBase):
    __tablename__ = 'evento_calendario'

    titulo = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.String(50))
    data = db.Column(db.DateTime, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('responsavel.id'), nullable=False)