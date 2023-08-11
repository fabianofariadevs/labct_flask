from api import ma
from ..models import mix_produto_model
from marshmallow import fields


class MixprodutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = mix_produto_model.Mixproduto
        load_instance = True
        fields = ("id", "cliente_id", "cod_prod_mix", "produto_id", "descricao", "modo_preparo", "departamento", "rend_kg", "rend_unid", "validade", "status", "cadastrado_em", "atualizado_em", "_links")

    cliente_id = fields.String(required=True)
    produto_id = fields.String(required=True)
    cod_prod_mix = fields.Integer(required=True)
    descricao = fields.String(required=True)
    modo_preparo = fields.String(required=True)
    departamento = fields.String(required=True)
    rend_kg = fields.Float(required=True)
    rend_unid = fields.Float(required=True)
    validade = fields.Date(required=True)
    status = fields.Integer(required=True)
    cadastrado_em = fields.DateTime(required=True)
    atualizado_em = fields.DateTime(required=True)

    _links = ma.Hyperlinks(
        {
            "get": ma.URLFor("mixprodutodetail", id="<id>"),
            "put": ma.URLFor("mixprodutodetail", id="<id>"),
            "delete": ma.URLFor("mixprodutodetail", id="<id>")
        }
    )