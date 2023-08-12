from api import db
from ..models.produtoMp_model import Produto
from sqlalchemy import func

#TODO ** Classe Estoque dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

class Estoque(db.Model):
    __tablename__ = "estoque"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    validade = db.Column(db.Date(), nullable=False)
    valor_ultima_compra = db.Column(db.Float, nullable=False)
    quantidade_op = db.Column(db.Integer, nullable=True, default=0)
    quantidade_minima = db.Column(db.Integer, nullable=True, default=0)
    obs = db.Column(db.Text(), nullable=True)
    #TODO relacionamento de N/1 com Produto / Cliente
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    produto = db.relationship(Produto, back_populates="estoques_produto")
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    cliente = db.relationship("Cliente", back_populates="estoques_cliente")#TODO (lazy="dynamic") só usamos com relacionamentos N/1

