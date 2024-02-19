from datetime import datetime
from api import db


# TODO ** Classe Mixproduto dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
class MixProduto(db.Model):
    __tablename__ = "mixproduto"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cod_prod_mix = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=datetime.now())
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    # TODO relacionamento com tabela receita 1/1
    receita_id = db.Column(db.Integer, db.ForeignKey("receita.id"), nullable=False)
    receita = db.relationship("Receita", back_populates="mixprodutos", foreign_keys=[receita_id])
    # TODO relacionamento com tabela pedido_producao 1/N
    #pedidosprod_id = db.Column(db.Integer, db.ForeignKey("pedidoproducao.id"), nullable=False)
    pedidosprod = db.relationship("PedidoProducao", back_populates="mixprodutos")
    #producao_id = db.Column(db.Integer, db.ForeignKey("producao.id", ondelete="CASCADE"), nullable=True)
    producoes = db.relationship("Producao", back_populates="mixprodutos", cascade="all, delete-orphan", uselist=False, single_parent=True, foreign_keys="[Producao.mixproduto_id]")
    # TODO relacionamento com tabela PRODUTOS N/N
    produtos = db.relationship("Produto", secondary="mixproduto_produto", back_populates="mixprodutos", single_parent=True, cascade="all, delete-orphan", lazy="joined")

    def json(self):
        return {
            "id": self.id,
            "cod_prod_mix": self.cod_prod_mix,
            "status": self.status,
            "cadastrado_em": self.cadastrado_em,
            "atualizado_em": self.atualizado_em,
            "receita_id": self.receita_id,
            "receita": self.receita.json(),
            "produtos": [produto.json() for produto in self.produtos]
        }
