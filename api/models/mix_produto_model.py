from datetime import datetime
from api import db
from ..models.pedido_model import PedidoProducao

# TODO RELACIONAMENTO N/N Mixproduto_Filial
#       @Author Fabiano Faria
mixproduto_filial = db.Table("mixproduto_filial", db.Column("mixproduto_id", db.Integer, db.ForeignKey("mixproduto.id"), primary_key=True),
                             db.Column("filial_id", db.Integer, db.ForeignKey("filial.id"), primary_key=True),
                             db.Column("qtde_produzida", db.Integer, nullable=True, default=0))

# TODO ** Classe Mixproduto dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
class MixProduto(db.Model):
    __tablename__ = "mixproduto"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cod_prod_mix = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, default=1, nullable=True)
    situacao = db.Column(db.String(50), nullable=False)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=datetime.now())
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    # TODO relacionamento com tabela filial N/N
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id', ondelete="CASCADE"), nullable=True)
    filiais = db.relationship("Filial", secondary="mixproduto_filial", back_populates="mixprodutos")
    # TODO relacionamento com tabela receita 1/1
    receita_id = db.Column(db.Integer, db.ForeignKey("receita.id"), nullable=False)
    receita = db.relationship("Receita", back_populates="mixprodutos", foreign_keys=[receita_id])
    # TODO relacionamento com tabela pedido_producao 1/N
    #pedidosprod_id = db.Column(db.Integer, db.ForeignKey("pedidoproducao.id"), nullable=False)
    pedidosprod = db.relationship("PedidoProducao", back_populates="mixprodutos")
    producao_id = db.Column(db.Integer, db.ForeignKey("producao.id"), nullable=True)
    producoes = db.relationship("Producao", back_populates="mixprodutos", cascade="all, delete-orphan", uselist=False, single_parent=True, foreign_keys="[Producao.mixproduto_id]")
    # TODO relacionamento com tabela PRODUTOS N/N
    produtos = db.relationship("Produto", secondary="mixproduto_produto", back_populates="mixprodutos", single_parent=True, cascade="all, delete-orphan", lazy="joined")
    #quantidades = db.relationship("QuantidadeMixProdutos", back_populates="mix_produtos", cascade="all, delete-orphan", lazy="joined")

# Novo modelo para armazenar quantidades
class QuantidadeMixProdutos(db.Model):
    __tablename__ = 'quantidade_mix_produtos'
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Float)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    mix_id = db.Column(db.Integer, db.ForeignKey('mixproduto.id'), nullable=False)
    #mix_produtos = db.relationship('MixProduto', back_populates='quantidades', foreign_keys=[mix_id])
    produto = db.relationship('Produto', back_populates='quantidades')

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


