from api import db
#from ..models.cliente_model import Cliente

class Mixproduto(db.Model):
    __tablename__ = "mixproduto"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    cod_prod_mix = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text(), nullable=False)
    modo_preparo = db.Column(db.Text(), nullable=False)
    departamento = db.Column(db.String(20), nullable=False)
    rend_kg = db.Column(db.Float, nullable=False)
    rend_unid = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=1, nullable=True)
    validade = db.Column(db.Date, nullable=False)
    cadastrado_em = db.Column(db.Date, nullable=False)
    atualizado_em = db.Column(db.Date, nullable=False)

    # TODO relacionando mixproduto com CLIENTE/Fabrica 1/N
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id', ondelete="CASCADE"), nullable=False)
    cliente = db.relationship("Cliente", back_populates="mixprodutos")

    #TODO Relacionamento com a tabela "Produto"
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"))
    produtos = db.relationship("Produto", back_populates="mixproduto")

