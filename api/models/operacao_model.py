from api import db
import enum

class TipoEnum(enum.Enum):
    compra = 1
    producao = 2

class Operacao(db.Model):
    __tablename__ = 'operacao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cliente_id = db.Column(db.String(50), nullable=False)#nome

    produto_id = db.Column(db.String(100), nullable=False)#resumo

    qtde = db.Column(db.Integer, nullable=False)#custo
    tipo = db.Column(db.Enum(TipoEnum), nullable=False)#tipo
    estoque_id = db.Column(db.Integer, db.ForeignKey("estoque.id"))#conta
