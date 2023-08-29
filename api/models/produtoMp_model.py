from api import db
from datetime import datetime
from sqlalchemy import func
from .fornecedor_model import Fornecedor
from .pedido_model import Pedido

receita_produto = db.Table('receita_produto',
                           db.Column('receita_id', db.Integer, db.ForeignKey('receita.id'), unique=True, nullable=False),
                           db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'), unique=True, nullable=False))

class Produto(db.Model):
    __tablename__ = "produto"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(150), nullable=False)
    quantidade = db.Column(db.Integer, nullable=True, default=0)
    compra_unid = db.Column(db.Integer, nullable=False)
    peso_pcte = db.Column(db.Numeric(5, 3), nullable=False)
    valor = db.Column(db.Numeric, nullable=False)
    custo_ultima_compra = db.Column(db.Float, nullable=False)
    whatsapp = db.Column(db.String(50), nullable=False)
    qrcode = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    #TODO Chave estrangeira referenciando o fornecedor
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    # Relacionamento com a tabela "Fornecedor"
    fornecedor = db.relationship(Fornecedor, back_populates="produtos")
    ##cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    estoques_produto = db.relationship("Estoque", back_populates="produto")
    mixproduto = db.relationship("Mixproduto", back_populates="produtos")
    # Relacionamento com a tabela "pedidos"
    pedidos = db.relationship(Pedido, back_populates="produtos")
    receitas_produtos = db.relationship("Receita", secondary="receita_produto", back_populates="produtos")


class Inventario(db.Model):
    __tablename__ = 'inventario'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(120))
    nome = db.Column(db.String(80))
    quantidade = db.Column(db.Integer, nullable=True, default=0)
    detalhes = db.Column(db.String(80))
    obs = db.Column(db.String(120))
    data = db.Column(db.Date, default=func.now())
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    produto = db.relationship(Produto, backref=db.backref("inventario", lazy="dynamic"))
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    cliente = db.relationship("Cliente", backref=db.backref("inventario", lazy="dynamic"))
