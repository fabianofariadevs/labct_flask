from api import db, ma
from datetime import datetime
from sqlalchemy import func
from ..models.mix_produto_model import Mixproduto

# TODO ** Classe Receita dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.

class Receita(db.Model):

    __tablename__ = "receita"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    descricao_mix = db.Column(db.Text(), nullable=False)
    modo_preparo = db.Column(db.Text(), nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    rend_kg = db.Column(db.Float, nullable=False)
    rend_unid = db.Column(db.Float, nullable=False)
    validade = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # TODO relacionando Receita c/ usuario 1/1
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    # TODO relacionando RECEITA c/ cliente e produtos N/N
    clientes = db.relationship("Cliente", secondary="receita_cliente", back_populates="receitas")

    # TODO relacionando RECEITA c/ produtos N/N = receita_produto TESTANDO C INGREDIENTES ABAIXO
    produtos = db.relationship("Produto", secondary="receita_produto", back_populates="receitas")

    # Relacionamento N/N com a tabela Ingredientes
    ingredientes = db.relationship("Ingredientes", back_populates="receita", cascade="all, delete-orphan", lazy="dynamic")

    # Relacionamento N/N com a tabela PedidoProducao
    pedidosprod = db.relationship("PedidoProducao", back_populates="receitas")

    # Relacionamento 1/1 com tabela mixproduto
    #mixproduto_id = db.Column(db.Integer, db.ForeignKey("mixproduto.id"), nullable=False)
    mixprodutos = db.relationship(Mixproduto, back_populates="receitas")

    def __repr__(self):
        return f"<Receita {self.descricao_mix}>"


class Ingredientes(db.Model):
    __tablename__ = "ingredientes"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(10), nullable=False)
    receita_id = db.Column(db.Integer, db.ForeignKey("receita.id"), nullable=False)
    receita = db.relationship(Receita, back_populates="ingredientes")
