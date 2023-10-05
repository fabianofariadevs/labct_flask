from api import db, ma
from ..models.produtoMp_model import Produto, receita_produto
from datetime import datetime
from sqlalchemy import func

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
    validade = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    # Propriedade 'filiais' referenciando a tabela "filial"
    # TODO relacionando RECEITA c/ Filiais N/N
    filiais = db.relationship("Filial", secondary="receita_filial", back_populates="receitas")
    quantidades = db.Column(db.Float, nullable=True, default=0)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    # TODO relacionando RECEITA c/ cliente e produtos N/N
    clientes = db.relationship("Cliente", secondary="receita_cliente", back_populates="receitas")

    # Relacionamento N/N com a tabela Produto
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    produtos = db.relationship("Produto", secondary=receita_produto, back_populates="receitas", lazy="dynamic")

    # Relacionamento N/N com a tabela PedidoProducao
    pedidosprod = db.relationship("PedidoProducao", back_populates="receitas")

    # Relacionamento 1/1 com tabela mixproduto
    #mixproduto_id = db.Column(db.Integer, db.ForeignKey("mixproduto.id"), nullable=False)
    mixprodutos = db.relationship("Mixproduto", back_populates="receitas")

    def __repr__(self):
        return f"<Receita {self.descricao_mix}>"


