from api import ma, db
from ..models import produtoMp_model, mix_produto_model
from marshmallow import fields

#TODO ** Classe ProdutoMpSchema_Modelo ** este esquema define como os objetos da classe Produto devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria


class ProdutoMpSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = produtoMp_model.Produto
        load_instance = True
        include_relationships = True # Inclui automaticamente os relacionamentos
        fields = ("id", "nome", "descricao", "quantidade", "compra_unid", "peso_pcte", "valor", "custo_ultima_compra", "whatsapp", "qrcode", "status", "estoque_minimo", "obs", "cadastrado_em", "atualizado_em",
                  "fornecedor", "estoques_produto", "pedidos_compra", "reposicoes", "inventario",
                  "quantidades")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    quantidade = fields.Integer(required=True)
    compra_unid = fields.Integer(required=True)
    peso_pcte = fields.Float(required=False)
    valor = fields.Decimal(required=True)
    custo_ultima_compra = fields.Decimal(required=False)
    whatsapp = fields.String(required=True)
    qrcode = fields.String(required=False)
    status = fields.Integer(required=False)
    estoque_minimo = fields.Integer(required=False)
    obs = fields.String(required=False)
    cadastrado_em = fields.DateTime(required=False, format="%Y-%m-%dT%H:%M:%S")
    atualizado_em = fields.DateTime(required=False, format="%Y-%m-%dT%H:%M:%S")

    fornecedor = ma.Nested("FornecedorSchema", many=False, only=('id', 'nome'))
    estoques_produto = ma.Nested("EstoqueSchema", many=False, only=('id', 'nome'))
    pedidos_compra = ma.Nested("PedidoSchema", many=False, only=('id', 'nome'))
    reposicoes = ma.Nested("ReposicaoEstoqueSchema", many=False, only=('id', 'produto_id', 'data_solicitacao'))
    inventario = ma.Nested("InventarioSchema", many=False, only=('id', 'produto', 'quantidade', 'data'))
    mixprodutos = ma.Nested("MixProdutoSchema", many=True, only=('id', 'cod_prod_mix', 'status'))
    quantidades = ma.Nested("QuantidadeMixProdutosSchema", many=True, only=('id', 'quantidade', 'produto', 'mix_produto'))
class InventarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = produtoMp_model.Inventario
        load_instance = True
        fields = ("id", "produto", "cliente", "descricao", "nome", "quantidade", "detalhes", "obs",
                  "data", "cadastrado_em", "atualizado_em", "filial")

    produto = fields.Integer(required=False)
    cliente = fields.Integer(required=False)
    descricao = fields.String(required=False)
    nome = fields.String(required=False)
    quantidade = fields.Integer(required=False)
    detalhes = fields.String(required=False)
    obs = fields.String(required=False)
    data = fields.Date(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)
    filial = fields.Integer(required=False)




