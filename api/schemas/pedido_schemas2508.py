from api import ma
from ..models import pedido_model
from marshmallow import fields
from marshmallow.validate import Length, Range, Regexp, ValidationError
from datetime import datetime

#TODO ** Classe PedidoSchema_Modelo ** este esquema define como os objetos da classe Pedido devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class CustomDateField(fields.Date):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value.date()  # Se já for um datetime, extrair a parte de data
        try:
            return datetime.strptime(value, '%d-%m-%Y').date()
        except (TypeError, ValueError):
            raise ValidationError('Not a valid date.')
class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = pedido_model.Pedido
        load_instance = True
        fields = ("id", "qtde_pedido", "data_pedido", "data_entrega", "status", "obs", "produto_id", "fornecedor_id", "filial_pdv", "cadastrado_em", "atualizado_em")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    qtde_pedido = fields.Integer(required=True)
    data_pedido = CustomDateField(format='%d-%m-%Y')
    data_entrega = CustomDateField(format='%d-%m-%Y')
    status = fields.Integer(required=True)
    obs = fields.String(required=True)
    produto_id = fields.Integer(required=False)
    fornecedor_id = fields.Integer(required=False)
    filial_pdv = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)


class PedidoProducaoSchema(ma.SQLAlchemyAutoSchema):
    #tipo = EnumField(pedido_model.TipoEnum)

    class Meta:
        model = pedido_model.PedidoProducao
        load_instance = True
        fields = ("id", "data_pedido", "data_entrega", "qtde_pedido","status", "obs", "receita_id", "filial_pdv", "cadastrado_em", "atualizado_em")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    data_pedido = fields.DateTime(required=True)
    data_entrega = fields.DateTime(required=True)
    qtde_pedido = fields.Integer(required=True)
    status = fields.Integer(required=False)
    obs = fields.String(required=True)
    receita_id = fields.Integer(required=False)
    filial_pdv = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)


