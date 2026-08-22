from . import db
from datetime import datetime

class ModeloBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now, nullable=False)
    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now, 
        nullable=False,
    ) 


    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    def atualizar(self, **kwargs):
        for chave, valor in kwargs.items():
            if valor is not None:
                setattr(self, chave, valor)
        db.session.commit()

    def to_dict(self):
        colunas = self.__mapper__.columns.keys()  # pega colunas de TODAS as tabelas da herança
        resultado = {}
        for coluna in colunas:
            valor = getattr(self, coluna)
            if isinstance(valor, datetime):
                valor = valor.isoformat()
            resultado[coluna] = valor
        return resultado


    @classmethod
    def buscar_por_id(cls, id):
        return cls.query.get(id)
