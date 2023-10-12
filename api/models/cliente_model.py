from api import db
from sqlalchemy import func
from datetime import datetime
from .filial_pdv_model import Filial

#TODO ** Classe Cliente dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

# TODO RELACIONAMENTO N/N Receita_Cliente
receita_cliente = db.Table('receita_cliente',
                           db.Column('receita_id', db.Integer, db.ForeignKey('receita.id'), primary_key=True,
                                     nullable=False),
                           db.Column('cliente_id', db.Integer, db.ForeignKey('cliente.id'), primary_key=True,
                                     nullable=False)
                           )

class Cliente(db.Model):
    __tablename__ = "cliente"
    __table_args__ = {"extend_existing": True}  # indica que a tabela deve ser estendida se ela já existir no banco de dados.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
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

    #TODO a coluna filial_id como uma chave estrangeira referenciando a coluna id da tabela "filial".
    filial_id = db.Column(db.Integer, db.ForeignKey("filial.id"), nullable=True)
    #TODO a propriedade filial, que é uma referência à instância de Filial associada a cada Cliente. O argumento backref define uma propriedade adicional no modelo Filial para acessar os clientes associados a uma filial.
    filiais = db.relationship(Filial, back_populates="clientes", foreign_keys=[filial_id])

    #TODO Relacionamento com a tabela Receita N/N
    receita = db.Column(db.Integer, db.ForeignKey("receita.id"), nullable=True)
    receitas = db.relationship("Receita", secondary="receita_cliente", back_populates="clientes")

    #TODO Relacionamento com a tabela Pedido N/1
    pedidos = db.relationship("Pedido", back_populates="clientes")

    # relacionamento com Estoque
    estoques_cliente = db.relationship("Estoque", back_populates="cliente")
