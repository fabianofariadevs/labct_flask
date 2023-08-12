from api import ma
from ..models import estoque_model
from marshmallow import fields
from ..schemas import operacao_schema

#TODO ** Classe EstoqueSchema_Modelo ** este esquema define como os objetos da classe Estoque devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class EstoqueSchema(ma.SQLAlchemyAutoSchema):
    operacoes = ma.Nested(operacao_schema.OperacaoSchema, many=True, only=('cliente_id', 'produto_id', 'tipo', 'qtde'))

    class Meta:
        model = estoque_model.Estoque
        load_instance = True
     ##   fields = ("id", "nome", "validade", "valor_ultima_compra", "quantidade_estoque", "quantidade_minima", "obs", "produto_id", "cliente_id")

        nome = fields.String(required=False)
        validade = fields.Date(required=True)
        valor_ultima_compra = fields.Float(required=False)
        quantidade_op = fields.Float(required=True)
        quantidade_minima = fields.Integer(required=False)
        obs = fields.String(required=False)

        produto_id = fields.Integer(required=False)
        cliente_id = fields.Integer(required=False)
