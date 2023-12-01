from api import db
from datetime import datetime
from sqlalchemy import func, DECIMAL
from .fornecedor_model import Fornecedor
from .mix_produto_model import MixProduto
from sqlalchemy.orm import relationship

mixproduto_produto = db.Table('mixproduto_produto',
                              db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'), primary_key=True),
                              db.Column('mixproduto_id', db.Integer, db.ForeignKey('mixproduto.id'), primary_key=True),
                              db.Column('quantidade', db.Float, nullable=False))

class Produto(db.Model):
    __tablename__ = "produto"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(250), nullable=False)
    quantidade = db.Column(db.Integer, nullable=True, default=0)
    compra_unid = db.Column(db.Integer, nullable=False)
    peso_pcte = db.Column(db.Float(precision=2), nullable=False)
    valor = db.Column(db.DECIMAL(10, 2), nullable=False)
    custo_ultima_compra = db.Column(db.DECIMAL(10, 2), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=False)
    qrcode = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    estoque_minimo = db.Column(db.Integer, nullable=True, default=0)
    obs = db.Column(db.Text(), nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # Relacionamento com a tabela "Fornecedor"
    #TODO Chave estrangeira referenciando o fornecedor 1/N
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    fornecedor = db.relationship(Fornecedor, back_populates="produtos", foreign_keys=[fornecedor_id])

    estoque_id = db.Column(db.Integer, db.ForeignKey('estoque.id'), nullable=True)
    estoques_produto = db.relationship("Estoque", back_populates="produto", foreign_keys=[estoque_id])

    # TODO Relacionamento com a Produto c tabela "pedidosCompra 1/N"
    #pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    pedidos_compra = db.relationship("Pedido", back_populates="produtos", secondary="pedido_produto", lazy="joined")

    # TODO Relacionamento com a tabela mixproduto N/N
    mixprodutos = db.relationship(MixProduto, secondary="mixproduto_produto", back_populates="produtos", single_parent=True, cascade="all, delete-orphan", lazy="joined")

    # Relacionamento com a tabela Receita N/N
    #receitas = db.relationship("Receita", secondary="receita_produto", back_populates="produtos_receita", lazy="dynamic")
    # Relacionamento com ReposicaoEstoque
    reposicoes = relationship("ReposicaoEstoque", back_populates="produtos")

    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'), nullable=True)
    inventario = db.relationship("Inventario", back_populates="produto", foreign_keys=[inventario_id])
    quantidades = db.relationship("QuantidadeMixProdutos", back_populates="produto", cascade="all, delete-orphan", lazy="joined")


class MixProdutoProduto(db.Model):
    __tablename__ = 'mixproduto_produto'
    __table_args__ = {"extend_existing": True}

    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id', ondelete='CASCADE'), primary_key=True)
    mixproduto_id = db.Column(db.Integer, db.ForeignKey('mixproduto.id', ondelete='CASCADE'), primary_key=True)
    quantidade = db.Column(db.Float, nullable=False)


class Inventario(db.Model):
    __tablename__ = 'inventario'
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(120))
    nome = db.Column(db.String(80))
    quantidade = db.Column(db.Integer, nullable=True, default=0)
    detalhes = db.Column(db.String(80))
    obs = db.Column(db.String(120))
    data = db.Column(db.Date, default=func.now())
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    produto = db.relationship("Produto", back_populates="inventario", uselist=False, cascade="all, delete-orphan", lazy="joined")

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    cliente = db.relationship("Cliente", backref=db.backref("inventario", lazy="dynamic"))

    filial_pdv = db.Column(db.Integer, db.ForeignKey("filial.id"), nullable=True)
    filial = db.relationship("Filial", backref=db.backref("inventario", lazy="dynamic"))


