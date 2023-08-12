from api import db
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from sqlalchemy import func


class Usuario(db.Model):
    __tablename__ = "usuario"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    #empresa = db.Column(db.String(100), nullable=False)#CLIENTE
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean)
    status = db.Column(db.Boolean, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    api_key = db.Column(db.String(100), nullable=True)

    empresa = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    cliente = db.relationship("Cliente", backref=db.backref("usuarios", lazy="dynamic"))

    cargo = db.Column(db.Integer, db.ForeignKey('funcao.id'), nullable=False)
    funcao = db.relationship('Funcao', back_populates="usuarios", foreign_keys=[cargo])



    def encriptar_senha(self):
        self.senha = pbkdf2_sha256.hash(self.senha)

    def ver_senha(self, senha):
        return pbkdf2_sha256.verify(senha, self.senha)


class Funcao(db.Model):
    __tablename__ = "funcao"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    usuarios = db.relationship('Usuario', back_populates="funcao")

    def __repr__(self):
        return f"<Funcao {self.nome}>"