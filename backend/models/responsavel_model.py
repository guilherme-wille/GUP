from . import db
from .usuario_model import Usuario

class Responsavel(Usuario):
    __tablename__ = 'responsavel'

    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    cargo = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'responsavel',
    }