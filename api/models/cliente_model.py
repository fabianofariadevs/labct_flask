from api import db, ma
from sqlalchemy import func
from datetime import datetime
from .filial_pdv_model import Filial

#TODO ** Classe Cliente dbModel, responsavel por definir e criar o Banco de dados com as migrations flask db.
#       @author Fabiano Faria

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
    filiais = db.relationship(Filial, back_populates="cliente", foreign_keys=[filial_id])

    #TODO Relacionamento com a tabela Receita 1/N
    #receita = db.Column(db.Integer, db.ForeignKey("receita.id"), nullable=True)
    receitas = db.relationship("Receita", back_populates="clientes")

    #TODO Relacionamento com a tabela PedidoCompra N/1
    pedidos = db.relationship("Pedido", back_populates="clientes")

    #TODO Relacionamento com a tabela PedidoProducao N/1
    #pedidosprod = db.relationship("PedidoProducao", back_populates="filiais")
    pedidosprod = db.relationship('PedidoProducao', primaryjoin="Cliente.id==PedidoProducao.cliente_id", backref='cliente', lazy='dynamic')

    # relacionamento com Estoque
    estoques_cliente = db.relationship("Estoque", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente {self.nome}>"

    def to_dict(self):
        return dict(id=self.id, nome=self.nome, endereco=self.endereco, bairro=self.bairro, cidade=self.cidade, estado=self.estado, telefone=self.telefone, email=self.email, responsavel=self.responsavel, whatsapp=self.whatsapp, cnpj=self.cnpj, status=self.status, cadastrado_em=self.cadastrado_em, atualizado_em=self.atualizado_em)

    def from_dict(self, data):
        for field in ['nome', 'endereco', 'bairro', 'cidade', 'estado', 'telefone', 'email', 'responsavel', 'whatsapp', 'cnpj', 'status', 'cadastrado_em', 'atualizado_em']:
            if field in data:
                setattr(self, field, data[field])

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        sqla_session = db.session
        load_instance = True # TODO Define se o esquema Cliente deve carregar uma instância do modelo ao fazer a desserialização. Nesse caso, está definido como True.
        include_fk = True
        include_relationships = True
        load_only = ("filial",)
        dump_only = ("id", "cadastrado_em", "atualizado_em")

    filiais = ma.Nested("FilialSchema", only=("id", "nome", "endereco", "bairro", "cidade", "estado", "responsavel", "whatsapp", "cnpj", "status", "cadastrado_em", "atualizado_em"))
    receitas = ma.Nested("ReceitaSchema", many=True, only=("id", "descricao_mix", "modo_preparo", "departamento", "rend_kg", "rend_unid", "validade", "status", "cadastrado_em", "atualizado_em"))
    pedidos = ma.Nested("PedidoSchema", many=True, only=("id", "qtde_pedido", "data_pedido", "data_entrega", "status", "obs", "cadastrado_em", "atualizado_em"))
    pedidosprod = ma.Nested("PedidoProducaoSchema", many=True, only=("id", "data_pedido", "data_entrega", "qtde_pedido", "status", "obs", "cadastrado_em", "atualizado_em"))



