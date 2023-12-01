from api import db, ma
from ..models.pedido_model import PedidoProducao
from datetime import datetime


# TODO ** Classe Produção dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.

class Producao(db.Model):
    __tablename__ = "producao"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    data_producao = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    qtde_produzida = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    obs = db.Column(db.Text(), nullable=True)
    qr_code = db.Column(db.String(50), nullable=True)
    cadastrado_em = db.Column(db.DateTime, default=db.func.now, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # TODO relacionamento com tabela MixProduto 1/1
    mixproduto_id = db.Column(db.Integer, db.ForeignKey("mixproduto.id"), nullable=False)
    mixprodutos = db.relationship("MixProduto", back_populates="producoes", foreign_keys=[mixproduto_id])

    # TODO relacionamento com tabela Filial 1/1
    filial_id = db.Column(db.Integer, db.ForeignKey("filial.id"), nullable=False)
    filial = db.relationship("Filial", back_populates="producoes")

    # TODO relacionamento com tabela Usuario 1/1
    usuario = db.relationship("Usuario", back_populates="producoes")

    # TODO relacionamento com tabela PedidoProducao 1/1
    pedidosprod = db.relationship("PedidoProducao", back_populates="producoes", foreign_keys=[PedidoProducao.producao_id])


