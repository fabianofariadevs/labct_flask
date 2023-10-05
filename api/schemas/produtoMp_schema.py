from api import ma
from ..models import produtoMp_model
from ..schemas.estoque_schema import EstoqueSchema, ReposicaoEstoqueSchema
from ..schemas import mix_produto_schema
from marshmallow import fields

#TODO ** Classe ProdutoMpSchema_Modelo ** este esquema define como os objetos da classe Produto devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class ProdutoMpSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = produtoMp_model.Produto
        load_instance = True
        fields = ("id", "nome", "descricao", "quantidade", "compra_unid", "peso_pcte", "valor", "custo_ultima_compra", "whatsapp", "qrcode", "status", "estoque_minimo", "obs", "cadastrado_em", "atualizado_em",
                  "fornecedor", "estoques_produto", "mixproduto", "pedidos", "receitas", "reposicoes")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    quantidade = fields.Integer(required=True)
    compra_unid = fields.Integer(required=True)
    peso_pcte = fields.Float(required=False)
    valor = fields.Float(required=True)
    custo_ultima_compra = fields.Float(required=False)
    whatsapp = fields.String(required=True)
    qrcode = fields.String(required=False)
    status = fields.Integer(required=True)
    estoque_minimo = fields.Integer(required=False)
    obs = fields.String(required=False)
    cadastrado_em = fields.Date(required=False)
    atualizado_em = fields.Date(required=False)
    fornecedor = fields.String(required=True)

    estoques_produto = fields.Nested("EstoqueSchema", many=True, exclude=("produto",))
    mixproduto = fields.Nested(mix_produto_schema.MixprodutoSchema, many=True, exclude=("produto",))
    pedidos = fields.Nested("PedidoSchema", many=True, exclude=("produto",))
    receitas = fields.List(fields.Nested("ReceitaSchema", many=True, exclude=("produto",)))
    reposicoes = fields.Nested(ReposicaoEstoqueSchema, many=True, exclude=("produto",))


class InventarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = produtoMp_model.Inventario
        load_instance = True
        fields = ("id", "produto_id", "cliente_id", "descricao", "nome", "quantidade", "detalhes", "obs", "data")

    produto_id = fields.Integer(required=False)
    cliente_id = fields.Integer(required=False)
    descricao = fields.String(required=False)
    nome = fields.String(required=False)
    quantidade = fields.Integer(required=False)
    detalhes = fields.String(required=False)
    obs = fields.String(required=False)
    data = fields.Date(required=False)



