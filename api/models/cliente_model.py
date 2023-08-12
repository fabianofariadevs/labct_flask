from api import db
from sqlalchemy import func
from datetime import datetime
from .filial_pdv_model import Filial
from .mix_produto_model import Mixproduto
from .estoque_model import Estoque

#TODO ** Classe Cliente dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

class Cliente(db.Model):
    __tablename__ = "cliente"
    __table_args__ = {"extend_existing": True} # indica que a tabela deve ser estendida se ela já existir no banco de dados.
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
    filial_id = db.Column(db.Integer, db.ForeignKey("filial.id"), nullable=False)
    #TODO a propriedade filial, que é uma referência à instância de Filial associada a cada Cliente. O argumento backref define uma propriedade adicional no modelo Filial para acessar os clientes associados a uma filial.
    filial = db.relationship(Filial, back_populates="clientes")

    estoques_cliente = db.relationship("Estoque", back_populates="cliente")    # relacionamento com Estoque
    #mix_id = db.Column(db.Integer, db.ForeignKey("mixproduto.id"), nullable=False)
    mixprodutos = db.relationship(Mixproduto, back_populates="cliente", cascade="all, delete-orphan", lazy="dynamic")