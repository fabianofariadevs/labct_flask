from api import db, ma
from datetime import datetime
from sqlalchemy import func
from .receita_model import Receita

# TODO ** Classe PedidoCompra dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

class Pedido(db.Model):
    __tablename__ = "pedido"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    qtde_pedido = db.Column(db.Integer, nullable=True, default=0)
    data_pedido = db.Column(db.DateTime, nullable=False, default=datetime.now())
    data_entrega = db.Column(db.Date, nullable=True)
    status = db.Column(db.Integer, default=1, nullable=True)
    obs = db.Column(db.Text(), nullable=False)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    produtos = db.relationship("Produto", secondary="pedido_produto", back_populates="pedidos_compra")
    clientes = db.relationship("Cliente", secondary="pedido_cliente", back_populates="pedido_compra")
    fornecedores = db.relationship("Fornecedor", secondary="pedido_fornecedor", back_populates="pedido_compra")

    #TODO relacionamento de N/1 com Produto / Pedido
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), unique=True)


# Adicione as tabelas intermediárias para os relacionamentos N-N
pedido_produto = db.Table(
    "pedido_produto",
    db.Column("pedido_id", db.Integer, db.ForeignKey("pedido.id"), primary_key=True),
    db.Column("produto_id", db.Integer, db.ForeignKey("produto.id"), primary_key=True)
)

pedido_cliente = db.Table(
    "pedido_cliente",
    db.Column("pedido_id", db.Integer, db.ForeignKey("pedido.id"), primary_key=True),
    db.Column("cliente_id", db.Integer, db.ForeignKey("cliente.id"), primary_key=True)
)

pedido_fornecedor = db.Table(
    "pedido_fornecedor",
    db.Column("pedido_id", db.Integer, db.ForeignKey("pedido.id"), primary_key=True),
    db.Column("fornecedor_id", db.Integer, db.ForeignKey("fornecedor.id"), primary_key=True)
)

# TODO ** Classe PedidoProdução dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
class PedidoProducao(db.Model):
    __tablename__ = "pedidoproducao"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    data_pedido = db.Column(db.DateTime, nullable=False, default=datetime.now())
    data_entrega = db.Column(db.Date, nullable=False)
    qtde_pedido = db.Column(db.Integer, nullable=True, default=0)
    situacao = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    obs = db.Column(db.Text(), nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    #TODO relacionamento de N/1 com Receita / pedidos PRODUÇÃO
    #receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'), nullable=True)
    #receitas = db.relationship("Receita", back_populates="pedidosprod", foreign_keys=[receita_id])

    # TODO relacionamento com tabela Filial N/N
    filiais = db.relationship("Filial", secondary="pedidoproducao_filial", back_populates="pedidosprod",)

    # TODO relacionamento com tabela Cliente 1/1
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    cliente = db.relationship("Cliente", back_populates="pedidosprod", foreign_keys=[cliente_id])

    # TODO relacionamento com tabela MixProduto 1/1
    mixproduto_id = db.Column(db.Integer, db.ForeignKey("mixproduto.id"), nullable=True)
    mixprodutos = db.relationship("MixProduto", back_populates="pedidosprod", foreign_keys=[mixproduto_id])

    # TODO relacionamento com tabela Producao 1/N
    producao_id = db.Column(db.Integer, db.ForeignKey("producao.id"), nullable=True)
    producoes = db.relationship("Producao", back_populates="pedidosprod", foreign_keys=[producao_id])

