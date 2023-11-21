from api import db, ma
from datetime import datetime
from sqlalchemy import func

# TODO ** Classe Receita dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.

class Receita(db.Model):
    __tablename__ = "receita"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    descricao_mix = db.Column(db.Text, nullable=False)
    modo_preparo = db.Column(db.Text, nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    rend_kg = db.Column(db.Float, nullable=False)
    rend_unid = db.Column(db.Float, nullable=False)
    validade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    # TODO relacionando Receita c/ usuario 1/1
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)
    # TODO relacionando RECEITA c/ cliente N/1
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    cliente = db.relationship("Cliente", back_populates="receitas", foreign_keys=[cliente_id])
    # TODO relacionando RECEITA c/ mixprodutos 1/1
    mixprodutos = db.relationship("MixProduto", back_populates="receita", uselist=False, cascade="all, delete-orphan", lazy="joined")
    # TODO Relacionamento 1/N com a tabela PedidoProducao
    pedidosprod = db.relationship("PedidoProducao", back_populates="receitas")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self