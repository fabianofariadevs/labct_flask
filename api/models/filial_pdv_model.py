from api import db
from sqlalchemy import func
from datetime import datetime
from .receita_model import Receita

# TODO ** Classe Filial dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

# RELACIONAMENTO N/N Receita_Filial
receita_filial = db.Table('receita_filial',
                          db.Column('receita_id', db.Integer, db.ForeignKey('receita.id'), primary_key=True,
                                    nullable=False),
                          db.Column('filial_id', db.Integer, db.ForeignKey('filial.id'), primary_key=True,
                                    nullable=False)
                          )

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
    estoques_filial = db.relationship("Estoque", back_populates="filial")  # relacionamento com Estoque

    # TODO Relacionamento com a tabela Receita N/N
    # receita = db.Column(db.Integer, db.ForeignKey("receita.id"), nullable=False)
    receitas = db.relationship(Receita, secondary="receita_filial", back_populates="filiais")

    # TODO Relacionamento com a tabela Pedido N/1
    # pedido = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    pedidos = db.relationship('Pedido', back_populates='filiais', foreign_keys='Pedido.filial_pdv')

   # cliente = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    clientes = db.relationship("Cliente", back_populates="filial", overlaps="filial")

    pedidosprod = db.relationship("PedidoProducao", back_populates="filiais")

