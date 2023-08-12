from api import db
from ..models import produtoMp_model
from datetime import datetime
from sqlalchemy import func

class Receita(db.Model):
    __tablename__ = "receita"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    descricao_mix = db.Column(db.Text(), nullable=False)
    modo_preparo = db.Column(db.Text(), nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    rend_kg = db.Column(db.Float, nullable=False)
    rend_unid = db.Column(db.Float, nullable=False)
    validade = db.Column(db.Date(), nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    # Propriedade 'filiais' referenciando a tabela "filial"
    # TODO relacionando RECEITA c/ Filiais N/N
    filiais = db.relationship("Filial", secondary="receita_filial", back_populates="receitas")

    # TODO relacionando RECEITA c/ cliente e produtos N/N
    #cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    #cliente = db.relationship(Cliente, backref=db.backref("receitas", lazy="dynamic"))
    #N/N
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    produtos = db.relationship(produtoMp_model.Produto, backref=db.backref("receitas", lazy="dynamic"))
    #1/N
    pedidosprod = db.relationship("PedidoProducao", back_populates="receitas")

