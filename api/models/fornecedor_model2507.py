from api import db
from sqlalchemy import func
from datetime import datetime
from ..models import produtoMp_model



class Fornecedor(db.Model):
    __tablename__ = "fornecedor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(150), nullable=False)
    bairro = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    responsavel = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(50), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False)
    status = db.Column(db.Boolean, default=1, nullable=False)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    atualizado_em = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    #TODO relacionando FORNECEDOR com CLIENTE/Fabrica e PRODUTO 1/N
    ##produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"))
    produtos = db.relationship("Produto",  back_populates="fornecedor", overlaps="fornecedores")
    #produtos = db.relationship(produtoMp_model.Produto, backref=db.backref("fornecedor", foreign_keys=[produtoMp_model.Produto.fornecedor_id]),                               lazy="dynamic")
    ##cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    ##cliente = db.relationship("Cliente", backref=db.backref("fornecedor", lazy="dynamic"))

