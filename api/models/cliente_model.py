from api import db, ma
from sqlalchemy import func
from datetime import datetime
from .filial_pdv_model import Filial
from .estoque_model import Estoque

#TODO ** Classe Cliente dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

class Cliente(db.Model):
    __tablename__ = "cliente"
    __table_args__ = {"extend_existing": True}  # indica que a tabela deve ser estendida se ela já existir no banco de dados.
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    endereco = db.Column(db.String(150), nullable=False)
    bairro = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    responsavel = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(50), nullable=False)
    cnpj = db.Column(db.String(17), nullable=True)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    #TODO a propriedade filial, 1/N, faz referência à instância de Filial associada a cada Cliente. O argumento backref define uma propriedade adicional no modelo Filial para acessar os clientes associados a uma filial.
    filiais = db.relationship(Filial, back_populates="cliente", overlaps="cliente", foreign_keys=[Filial.cliente_id])

    #TODO Relacionamento com a tabela Receita 1/N
    receitas = db.relationship("Receita", back_populates="cliente", foreign_keys="Receita.cliente_id")

    #TODO Relacionamento com a tabela PedidoCompra 1/N
    pedido_compra = db.relationship("Pedido", back_populates="clientes")

    #TODO Relacionamento com a tabela PedidoProducao 1/N
    pedidosprod = db.relationship("PedidoProducao", back_populates="cliente")

    # TODO Relacionamento com a tabela Usuario 1/N
    usuarios = db.relationship("Usuario", back_populates="cliente", foreign_keys="Usuario.empresa")

    # TODO Relacionamento com Estoque 1/N
    estoques = db.relationship("Estoque", back_populates="cliente", foreign_keys=[Estoque.cliente_id])

    # TODO Relacionamento com a tabela Cliente 1/N
    funcoes = db.relationship("Funcao", back_populates="cliente", foreign_keys="Funcao.cliente_id")

