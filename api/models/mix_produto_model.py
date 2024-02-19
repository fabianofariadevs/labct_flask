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
    # TODO relacionamento com tabela producao 1/1
    producoes = db.relationship("Producao", back_populates="mixprodutos", cascade="all, delete-orphan", uselist=False, single_parent=True, foreign_keys="[Producao.mixproduto_id]")
    # TODO relacionamento com tabela PRODUTOS N/N
    produtos = db.relationship("Produto", secondary="mixproduto_produto", back_populates="mixprodutos", single_parent=True, cascade="all, delete-orphan", lazy="joined")
    # TODO relacionamento com tabela QUANTIDADE MIXPRODUTO 1/N
    quantidades = db.relationship("QuantidadeMixProdutos", back_populates="mix_produto", cascade="all, delete-orphan", lazy="joined")

    def json(self):
        return {
            "id": self.id,
            "cod_prod_mix": self.cod_prod_mix,
            "status": self.status,
            "cadastrado_em": self.cadastrado_em,
            "atualizado_em": self.atualizado_em,
            "receita_id": self.receita_id,
            "receita": self.receita.json(),
            "produtos": [produto.json() for produto in self.produtos],
            "quantidades": [quantidades.json() for quantidades in self.quantidades]
        }

class QuantidadeMixProdutos(db.Model):
    __tablename__ = 'quantidade_mix_produtos'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=True)
    produto = db.relationship('Produto', back_populates='quantidades')
    mix_id = db.Column(db.Integer, db.ForeignKey('mixproduto.id'), nullable=True)
    mix_produto = db.relationship('MixProduto', back_populates='quantidades', foreign_keys=[mix_id])
    quantidade = db.Column(db.Float, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "produto": self.produto.json(),
            "mix_id": self.mix_id,
            "mix_produto": self.mix_produto.json(),
            "quantidade": self.quantidade
        }
