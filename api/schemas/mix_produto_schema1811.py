from api import ma
from ..models import mix_produto_model
from marshmallow import fields, EXCLUDE
from .produtoMp_schema import ProdutoMpSchema


class MixProdutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = mix_produto_model.MixProduto
        load_instance = True
        include_relationships = True
        fields = ("id", "cod_prod_mix", "status", "situacao", "quantidade", "cadastrado_em", "atualizado_em",
                  "receita", "pedidosprod", "producoes", "produtos")

    cod_prod_mix = fields.Integer(required=True)
    status = fields.Integer(required=False)
    situacao = fields.String(required=False)
    quantidade = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)

    receita = ma.Nested("ReceitaSchema", many=False, exclude=("mixprodutos",), unknown=EXCLUDE)  # Certifique-se de ajustar 'ReceitaSchema' conforme necessário)
    #filiais = ma.Nested("FilialSchema", many=True, exclude=("mixprodutos",), unknown="exclude")
    pedidosprod = ma.Nested("PedidoProducaoSchema", many=True, exclude=("mixprodutos",), unknown="exclude", only=('data_pedido', 'data_entrega', 'qtde_pedido', 'status', 'obs', 'cadastrado_em', 'atualizado_em', 'receitas', 'filiais', 'cliente', 'mixprodutos', 'producoes'))
    producoes = ma.Nested("ProducaoSchema", many=False, only=('data_producao',), exclude=("mixprodutos",), unknown="exclude")
    #produtos = ma.Nested("ProdutoMpSchema", many=True, exclude=("mixprodutos",), unknown="exclude")
    produtos = fields.List(fields.Nested(ProdutoMpSchema, exclude=("mixprodutos",), unknown="exclude"))

class QuantidadeMixProdutosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = mix_produto_model.QuantidadeMixProdutos
        load_instance = True
        include_relationships = True
        fields = ("id", "quantidade", "mix_produtos", "produto")

    quantidade = fields.Integer(required=True)
    mix_produtos = ma.Nested("MixProdutoSchema", many=False, exclude=("produtos",))
    produto = ma.Nested("ProdutoMpSchema", many=False, exclude=("mixprodutos",))


class ProducaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = mix_produto_model.Producao
        load_instance = True
        include_relationships = True  # Inclui automaticamente os relacionamentos
        fields = ("id", "data_producao", "qtde_produzida", "status", "obs", "qr_code", "cadastrado_em", "atualizado_em",
                  "mixprodutos", "filial", "usuario", "pedidosprod")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    data_producao = fields.Date(required=True)
    qtde_produzida = fields.Integer(required=True)
    status = fields.Integer(required=False)
    obs = fields.String(required=False)
    qr_code = fields.String(required=False)
    cadastrado_em = fields.DateTime(required=True)
    atualizado_em = fields.DateTime(required=True)

    mixprodutos = ma.Nested("MixProdutoSchema", many=False)
    filial = ma.Nested("FilialSchema", many=False)
    usuario = ma.Nested("UsuarioSchema", many=False)
    pedidosprod = ma.Nested("PedidoProducaoSchema", many=False)