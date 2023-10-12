from api import db
from sqlalchemy import func
from datetime import datetime
from ..models.estoque_model import Estoque

# TODO ** Classe Filial dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

class Filial(db.Model):
    __tablename__ = "filial"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(150), nullable=False)
    bairro = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    responsavel = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(50), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    estoques_filial = db.relationship(Estoque, back_populates="filial")

    # TODO Relacionamento com a tabela Mixproduto N/N
    #mixproduto = db.Column(db.Integer, db.ForeignKey("mixproduto.id"), nullable=False)
    mixprodutos = db.relationship("Mixproduto", secondary="mixproduto_filial", back_populates="filiais")

    # TODO Relacionamento com a tabela Filial N/1
   # cliente = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    clientes = db.relationship("Cliente", back_populates="filiais", overlaps="filiais")

    pedidosprod = db.relationship("PedidoProducao", back_populates="filiais")

