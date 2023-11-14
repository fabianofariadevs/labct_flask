from api import db
from sqlalchemy import func
from datetime import datetime

# TODO ** Classe Filial dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

estoque_filial = db.Table("estoque_filial", db.Column("estoque_id", db.Integer, db.ForeignKey("estoque.id"), primary_key=True),
                          db.Column("filial_id", db.Integer, db.ForeignKey("filial.id"), primary_key=True))

class Filial(db.Model):
    __tablename__ = "filial"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

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

    # TODO Relacionamento com a tabela Estoque N/N
    estoques = db.relationship("Estoque", secondary="estoque_filial", back_populates="filiais")

    # TODO Relacionamento com a tabela Mixproduto N/N
    #mixproduto = db.Column(db.Integer, db.ForeignKey("mixproduto.id"), nullable=False)
    mixprodutos = db.relationship("MixProduto", secondary="mixproduto_filial", back_populates="filiais")

    # TODO Relacionamento com a tabela Filial 1/1
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    cliente = db.relationship("Cliente", back_populates="filiais", overlaps="filiais", foreign_keys=[cliente_id])

    #pedidosprod_id = db.Column(db.Integer, db.ForeignKey("pedidoproducao.id"), nullable=False)
    pedidosprod = db.relationship("PedidoProducao", back_populates="filiais")

    producoes = db.relationship("Producao", back_populates="filial", uselist=False, cascade="all, delete-orphan", lazy="joined")
