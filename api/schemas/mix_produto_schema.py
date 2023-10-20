from api import ma
from ..models import mix_produto_model
from marshmallow import fields


class MixprodutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = mix_produto_model.Mixproduto
        load_instance = True
        fields = ("id", "cod_prod_mix", "status", "cadastrado_em", "atualizado_em",
                  "receita", "filiais", "usuarios")

    cod_prod_mix = fields.Integer(required=True)
    status = fields.Integer(required=True)
    cadastrado_em = fields.DateTime(required=True)
    atualizado_em = fields.DateTime(required=True)

    receita = fields.Nested("ReceitaSchema", many=True)
    filiais = fields.Nested("FilialSchema", many=True)
    usuarios = fields.Nested("UsuarioSchema", many=True)
