from api import ma
from ..models import pedido_model
from marshmallow import fields

#TODO ** Classe PedidoSchema_Modelo ** este esquema define como os objetos da classe Pedido devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = pedido_model.Pedido
        load_instance = True
        fields = ("id", "qtde_pedido", "data_pedido", "data_entrega", "status", "obs", "produto_id", "fornecedor_id", "filial_pdv", "cadastrado_em", "atualizado_em")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    qtde_pedido = fields.Integer(required=True)
    data_pedido = fields.DateTime(required=False)
    data_entrega = fields.Date(required=True)
    status = fields.Integer(required=True)
    obs = fields.String(required=True)
    produto_id = fields.Integer(required=False)
    fornecedor_id = fields.Integer(required=False)
    filial_pdv = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)


# TODO ** Classe PedidoProdução Schema_Modelo ** este esquema define como os objetos da classe Pedido devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
class PedidoProducaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = pedido_model.PedidoProducao
        load_instance = True
        include_relationships = True  # Inclui automaticamente os relacionamentos
        fields = ("id", "data_pedido", "data_entrega", "qtde_pedido", "status", "obs", "quantidade", "produto_id", "receita_id", "filial_pdv", "cadastrado_em", "atualizado_em")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    data_pedido = fields.DateTime(required=False)
    data_entrega = fields.Date(required=True)
    qtde_pedido = fields.Integer(required=True)
    status = fields.Integer(required=False)
    obs = fields.String(required=True)
    quantidade = fields.Integer(required=True)
    produto_id = fields.Integer(required=False)
    receita_id = fields.Integer(required=False)
    filial_pdv = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)



