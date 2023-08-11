from api import ma
from ..models import operacao_model
from marshmallow import fields
from marshmallow_enum import EnumField

class OperacaoSchema(ma.SQLAlchemyAutoSchema):
    tipo = EnumField(operacao_model.TipoEnum)

    class Meta:
        model = operacao_model.Operacao
        load_instance = True
        

        cliente_id = fields.Integer(required=True)

        produto_id = fields.Integer(required=True)

        qtde = fields.Float(required=True)
        estoque_id = fields.Integer(required=True)


