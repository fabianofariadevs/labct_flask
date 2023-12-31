from api import db

# TODO ** Classe Mixproduto dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @Author Fabiano Faria

# RELACIONAMENTO N/N Mixproduto_Filial
mixproduto_filial = db.Table('mixproduto_filial', db.Column('mixproduto_id', db.Integer, db.ForeignKey('mixproduto.id'), primary_key=True),
                             db.Column('filial_id', db.Integer, db.ForeignKey('filial.id'), primary_key=True)
)

class Mixproduto(db.Model):
    __tablename__ = "mixproduto"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cod_prod_mix = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.Date, nullable=False)
    atualizado_em = db.Column(db.Date, nullable=False)

    # TODO relacionamento com tabela receita 1/1
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id', ondelete="CASCADE"), nullable=False)
    receita = db.relationship("Receita", back_populates="mixproduto")

    # TODO relacionamento com tabela filial N/N
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id', ondelete="CASCADE"), nullable=False)
    filiais = db.relationship("Filial", secondary="mixproduto_filial", back_populates="mixprodutos")

    # TODO relacionamento usuario 1/1
    usuarios = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)



