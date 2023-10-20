from api import ma
from ..models import pedido_model
from marshmallow import fields

#TODO ** Classe PedidoSchema_Modelo ** este esquema define como os objetos da classe Pedido devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = pedido_model.Pedido
        load_instance = True
        fields = ("id", "qtde_pedido", "data_pedido", "data_entrega", "status", "obs", "cadastrado_em", "atualizado_em",
                  "produtos", "fornecedores", "clientes")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    qtde_pedido = fields.Integer(required=True)
    data_pedido = fields.DateTime(required=False)
    data_entrega = fields.Date(required=True)
    status = fields.Integer(required=True)
    obs = fields.String(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)

    produtos = fields.Nested("ProdutoSchema", only=('id', 'descricao'))
    fornecedores = fields.Nested("FornecedorSchema", only=('id', 'nome'))
    clientes = fields.Nested("ClienteSchema", only=('id', 'nome'))


# TODO ** Classe PedidoProdução Schema_Modelo ** este esquema define como os objetos da classe Pedido devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
class PedidoProducaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = pedido_model.PedidoProducao
        load_instance = True
        include_relationships = True  # Inclui automaticamente os relacionamentos
        fields = ("id", "data_pedido", "data_entrega", "qtde_pedido", "status", "obs", "cadastrado_em", "atualizado_em",
                  "receitas", "filiais")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    data_pedido = fields.DateTime(required=False)
    data_entrega = fields.Date(required=True)
    qtde_pedido = fields.Integer(required=True)
    status = fields.Integer(required=False)
    obs = fields.String(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)

    #TODO relacionamento de N/1 com Receita / pedidos PRODUÇÃO
    receita_id = fields.Integer(required=True)
    receitas = fields.Nested("ReceitaSchema", only=('id', 'nome'))

    #TODO relacionamento de N/1 com Filial / pedidos PRODUÇÃO
    filial_pdv = fields.Integer(required=True)
    filiais = fields.Nested("FilialSchema", only=('id', 'nome'))




