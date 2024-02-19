from api import ma
from ..models import pedido_model
from marshmallow import fields

#TODO ** Classe PedidoSchema_Modelo ** este esquema define como os objetos da classe Pedido devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = pedido_model.Pedido
        load_instance = True
        include_relationships = True # Inclui automaticamente os relacionamentos
        fields = ("id", "qtde_pedido", "data_pedido", "data_entrega", "status", "obs", "cadastrado_em", "atualizado_em",
                  "produtos", "fornecedores", "clientes")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    data_pedido = fields.DateTime(required=False)
    data_entrega = fields.Date(required=True)
    qtde_pedido = fields.Integer(required=True)
    status = fields.Integer(required=True)
    obs = fields.String(required=True)
    cadastrado_em = fields.DateTime(required=False, dump_only=True)
    atualizado_em = fields.DateTime(required=False, dump_only=True)

    produtos = fields.Integer(required=False)
    fornecedores = fields.Integer(required=False)
    clientes = fields.Integer(required=False)

    #produtos = ma.Nested("ProdutoMpSchema", many=True, only=('id', 'nome', 'status'))
    #fornecedores = ma.Nested("FornecedorSchema", many=False, only=('id',))
    #clientes = ma.Nested("ClienteSchema", many=False, only=('id',))


# TODO ** Classe PedidoProdução Schema_Modelo ** este esquema define como os objetos da classe Pedido devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
class PedidoProducaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = pedido_model.PedidoProducao
        load_instance = True
        include_relationships = True  # Inclui automaticamente os relacionamentos
        fields = ("id", "data_pedido", "data_entrega", "qtde_pedido", "status", "obs", "cadastrado_em", "atualizado_em",
                  "receitas", "filiais", "cliente", "mixprodutos", "producoes")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    data_pedido = fields.DateTime(required=False)
    data_entrega = fields.Date(required=True)
    qtde_pedido = fields.Integer(required=True)
    status = fields.Integer(required=False)
    obs = fields.String(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)

    receitas = ma.Nested("ReceitaSchema", many=False, only=('id', 'descricao_mix', 'status'))
    filiais = ma.Nested("FilialSchema", many=False, only=('id', 'nome'))
    cliente = ma.Nested("ClienteSchema", many=False, only=('id', 'nome'))
    mixprodutos = ma.Nested("MixProdutoSchema", many=False, only=('id', 'cod_prod_mix', 'situacao', 'status'))
    producoes = ma.Nested("ProducaoSchema", many=True, only=('id', 'data_producao', 'status', 'obs', 'filial', 'pedidosprod', 'mixprodutos'))




