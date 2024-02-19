from api import db
from ..models.produtoMp_model import Produto
from sqlalchemy import func

#TODO ** Classe Estoque dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

class Estoque(db.Model):
    __tablename__ = "estoque"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(80), nullable=True)
    validade = db.Column(db.Date(), nullable=False)
    valor_ultima_compra = db.Column(db.Float, nullable=False)
    quantidade_minima = db.Column(db.Integer, nullable=True, default=0)
    obs = db.Column(db.Text(), nullable=True)
    quantidade_atual = db.Column(db.Integer, nullable=True, default=0)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    #TODO relacionamento de 1/N com Produto / Cliente
    #produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    produto = db.relationship(Produto, back_populates="estoques_produto")

    fornecedor_id = db.Column(db.Integer, db.ForeignKey("fornecedor.id"), nullable=True)
    fornecedor = db.relationship("Fornecedor", back_populates="estoques", foreign_keys=[fornecedor_id])

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    cliente = db.relationship("Cliente", back_populates="estoques", foreign_keys=cliente_id)   # TODO (lazy="dynamic") só usamos com relacionamentos N/1

    #TODO relacionamento com a tabela Filial N/N
    filiais = db.relationship("Filial", secondary="estoque_filial", back_populates="estoques")

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'validade': self.validade,
            'valor_ultima_compra': self.valor_ultima_compra,
            'quantidade_minima': self.quantidade_minima,
            'obs': self.obs,
            'quantidade_atual': self.quantidade_atual,
            'status': self.status,
            'cadastrado_em': self.cadastrado_em.strftime("%d/%m/%Y %H:%M:%S"),
            'atualizado_em': self.atualizado_em.strftime("%d/%m/%Y %H:%M:%S")
        }

class ReposicaoEstoque(db.Model):
    __tablename__ = "reposicao_estoque"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    produtos = db.relationship("Produto", back_populates="reposicoes")
    data_solicitacao = db.Column(db.DateTime, nullable=False, default=func.now)
