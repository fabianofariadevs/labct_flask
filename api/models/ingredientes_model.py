from api import db, ma
#from ..models.receita_model import Receita

# TODO ** Classe Ingredientes dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.

class Ingredientes(db.Model):
    __tablename__ = "ingredientes"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(10), nullable=False)
    receita_id = db.Column(db.Integer, db.ForeignKey("receita.id"), nullable=False)
   # receita = db.relationship("Receita", back_populates="ingredientes", foreign_keys=[receita_id])
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
   # produto = db.relationship("Produto", back_populates="ingredientes")

