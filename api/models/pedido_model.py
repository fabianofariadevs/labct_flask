from api import db
from datetime import datetime
from sqlalchemy import func
from .receita_model import Receita

# TODO ** Classe Pedido dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

class Pedido(db.Model):
    __tablename__ = "pedido"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    qtde_pedido = db.Column(db.Integer, nullable=True, default=0)
    data_pedido = db.Column(db.DateTime, nullable=False, default=func.now)
    data_entrega = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    obs = db.Column(db.Text(), nullable=False)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    #TODO relacionamento de N/1 com Produto / Pedido
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    produtos = db.relationship("Produto", back_populates="pedidos", foreign_keys=[produto_id])

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    clientes = db.relationship("Cliente", back_populates="pedidos")

    fornecedor = db.Column(db.Integer, db.ForeignKey("fornecedor.id"), nullable=True)
    fornecedores = db.relationship("Fornecedor", back_populates="pedidos")

class PedidoProducao(db.Model):
    __tablename__ = "pedidoproducao"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    data_pedido = db.Column(db.DateTime, nullable=False, default=func.now)
    data_entrega = db.Column(db.Date, nullable=False)
    qtde_pedido = db.Column(db.Integer, nullable=True, default=0)
    status = db.Column(db.Integer, default=1, nullable=True)
    obs = db.Column(db.Text(), nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    #TODO relacionamento de N/1 com Receita / pedidos PRODUÇÃO
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'), nullable=False)
    receitas = db.relationship(Receita, back_populates="pedidosprod", foreign_keys=[receita_id])

    filial_pdv = db.Column(db.Integer, db.ForeignKey("filial.id"), nullable=True)
    filiais = db.relationship("Filial", back_populates="pedidosprod", foreign_keys=[filial_pdv])

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
