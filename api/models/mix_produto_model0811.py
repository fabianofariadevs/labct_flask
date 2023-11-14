from datetime import datetime
from api import db
from ..models.pedido_model import PedidoProducao

# TODO ** Classe Mixproduto dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @Author Fabiano Faria

# RELACIONAMENTO N/N Mixproduto_Filial
#mixproduto_filial = db.Table('mixproduto_filial', db.Column('mixproduto_id', db.Integer, db.ForeignKey('mixproduto.id'), primary_key=True),
 #                            db.Column('filial_id', db.Integer, db.ForeignKey('filial.id'), primary_key=True)
  #                           )
class MixProdutoFilial(db.Model):
    __tablename__ = "mixproduto_filial"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    mixproduto_id = db.Column(db.Integer, db.ForeignKey('mixproduto.id'), nullable=False)
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id'), nullable=False)

    def mixprodutofilial_query(self):
        return MixProdutoFilial.query.get(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


class MixProduto(db.Model):
    __tablename__ = "mixproduto"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cod_prod_mix = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, default=1, nullable=True)
    situacao = db.Column(db.String(50), nullable=False)
    cadastrado_em = db.Column(db.Date, nullable=False)
    atualizado_em = db.Column(db.Date, nullable=False)

    # TODO relacionamento com tabela receita 1/1
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id', ondelete="CASCADE"), nullable=False)
    receita = db.relationship("Receita", back_populates="mixprodutos")

    # TODO relacionamento com tabela filial N/N
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id', ondelete="CASCADE"), nullable=False)
    filiais = db.relationship("Filial", secondary="mixproduto_filial", back_populates="mixprodutos")

    # TODO relacionamento com tabela pedido_producao 1/N
    pedidosprod_id = db.Column(db.Integer, db.ForeignKey("pedidoproducao.id"), nullable=False)
    pedidosprod = db.relationship("PedidoProducao", back_populates="mixproduto", foreign_keys=[pedidosprod_id], lazy="joined")

    producao_id = db.Column(db.Integer, db.ForeignKey("producao.id"), nullable=True)
    producoes = db.relationship("Producao", back_populates="mixprodutos", uselist=True, single_parent=True, cascade="all, delete-orphan", foreign_keys="[Producao.mixproduto_id]")

    def mixproduto_query(self):
        return MixProduto.query.get(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @staticmethod
    def get_all():
        return MixProduto.query.all()

    @staticmethod
    def get_by_id(id):
        return MixProduto.query.get(id)

    def __repr__(self):
        return f"<MixProduto {self.cod_prod_mix, self.cadastrado_em, self.filiais, self.situacao, self.receita}>"

class Producao(db.Model):
    __tablename__ = "producao"
    __table_args__ = {"extend_existing": True}
    include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    data_producao = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    qtde_produzida = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    obs = db.Column(db.Text(), nullable=True)
    qr_code = db.Column(db.String(50), nullable=True)
    cadastrado_em = db.Column(db.DateTime, default=db.func.now, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # TODO relacionamento com tabela MixProduto 1/1
    mixproduto_id = db.Column(db.Integer, db.ForeignKey("mixproduto.id"), nullable=False)
    mixprodutos = db.relationship("MixProduto", back_populates="producoes", foreign_keys=[mixproduto_id])

    # TODO relacionamento com tabela Filial 1/1
    filial_id = db.Column(db.Integer, db.ForeignKey("filial.id"), nullable=False)
    filial = db.relationship("Filial", back_populates="producoes")

    # TODO relacionamento com tabela Usuario 1/1
    usuario = db.relationship("Usuario", back_populates="producoes")

    # TODO relacionamento com tabela PedidoProducao 1/1
    pedidosprod = db.relationship("PedidoProducao", back_populates="producoes", foreign_keys=[PedidoProducao.producao_id])

    def to_dict(self):
        return {
            'id': self.id,
            'data_producao': self.data_producao.strftime("%d/%m/%Y %H:%M:%S"),
            'qtde_produzida': self.qtde_produzida,
            'status': self.status,
            'obs': self.obs,
            'qr_code': self.qr_code,
            'cadastrado_em': self.cadastrado_em.strftime("%d/%m/%Y %H:%M:%S"),
            'atualizado_em': self.atualizado_em.strftime("%d/%m/%Y %H:%M:%S")
        }

    def producao_query(self):
        return Producao.query.get(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @staticmethod
    def get_all():
        return Producao.query.all()

    @staticmethod
    def get_by_id(id):
        return Producao.query.get(id)

    def __repr__(self):
        return f"<Producao {self.mixproduto, self.filial_id}>"


