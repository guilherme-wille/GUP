from . import db
from .base_model import ModeloBase

class Usuario(ModeloBase):
    __tablename__ = 'usuario'

    nome = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    data_nasc = db.Column(db.DateTime, nullable=False)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta_familia.id'))
    tipo_usuario = db.Column(db.String(20), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo_usuario,
    }
    