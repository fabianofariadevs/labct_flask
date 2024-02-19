from api import db
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from sqlalchemy import func
from ..models.producao_model import Producao


#TODO ** Classe Usuário dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria
class Usuario(db.Model):
    __tablename__ = "usuario"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Integer, default=0, nullable=True)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    api_key = db.Column(db.String(100), nullable=True)

    empresa = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    cliente = db.relationship("Cliente", back_populates="usuarios", foreign_keys=[empresa])

    cargo = db.Column(db.Integer, db.ForeignKey('funcao.id'), nullable=False)
    funcao = db.relationship('Funcao', back_populates="usuarios", foreign_keys=[cargo])

    producao_id = db.Column(db.Integer, db.ForeignKey("producao.id"), nullable=True)
    producoes = db.relationship(Producao, back_populates="usuario", foreign_keys=[producao_id])

    def encriptar_senha(self):
        self.senha = pbkdf2_sha256.hash(self.senha)

    def ver_senha(self, senha):
        return pbkdf2_sha256.verify(senha, self.senha)


class Funcao(db.Model):
    __tablename__ = "funcao"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    cadastrado_em = db.Column(db.DateTime, nullable=True, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # TODO Relacionamento com a tabela Usuario 1/N
    usuarios = db.relationship('Usuario', back_populates="funcao")

    # TODO Relacionamento com a tabela Cliente N/1
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    cliente = db.relationship("Cliente", back_populates="funcoes", foreign_keys=[cliente_id])

    def __repr__(self):
        return f"<Funcao {self.nome}>"
