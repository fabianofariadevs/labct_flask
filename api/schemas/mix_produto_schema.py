from api import ma
from ..models import mix_produto_model, producao_model
from marshmallow import fields, EXCLUDE

class MixProdutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = mix_produto_model.MixProduto
        load_instance = True
        include_relationships = True
        fields = ("id", "cod_prod_mix", "status", "cadastrado_em", "atualizado_em",
                  "receita", "pedidosprod", "producoes", "produtos", "quantidades")

    cod_prod_mix = fields.Integer(required=True)
    status = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)

    receita = ma.Nested("ReceitaSchema", many=False, unknown=EXCLUDE,)  # Certifique-se de ajustar 'ReceitaSchema' conforme necessário
    pedidosprod = ma.Nested("PedidoProducaoSchema", many=True, exclude=("mixprodutos",), unknown="exclude")
    producoes = ma.Nested("ProducaoSchema", many=False, exclude=("mixprodutos",), unknown="exclude",)
    produtos = ma.Nested("ProdutoMpSchema", many=True, unknown="exclude",)
    quantidades = ma.Nested("QuantidadeMixProdutosSchema", many=True, unknown="exclude")


class ProducaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = producao_model.Producao
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

    mixprodutos = ma.Nested("MixProdutoSchema", many=False, only=('id', 'cod_prod_mix', 'status', 'receita'))
    filial = ma.Nested("FilialSchema", many=False,)
    usuario = ma.Nested("UsuarioSchema", many=False, exclude=("producoes",))
    pedidosprod = ma.Nested("PedidoProducaoSchema", many=False,)

class QuantidadeMixProdutosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = mix_produto_model.QuantidadeMixProdutos
        load_instance = True
        include_relationships = True
        fields = ("id", "mix_produto", "produto", "quantidade")

    mix_produto = ma.Nested("MixProdutoSchema", many=False, exclude=("quantidades",))
    produto = ma.Nested("ProdutoMpSchema", many=False, exclude=("quantidades",))
    quantidade = fields.Float(required=False)
