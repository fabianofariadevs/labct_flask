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
        fields = ("id", "nome", "validade", "valor_ultima_compra", "quantidade_op", "quantidade_minima", "obs", "produto", "cliente")

    nome = fields.String(required=False)
    validade = fields.Date(required=True)
    valor_ultima_compra = fields.Float(required=False)
    quantidade_op = fields.Float(required=True)
    quantidade_minima = fields.Integer(required=False)
    obs = fields.String(required=False)
    produto = fields.Integer(required=False)
    cliente = fields.Integer(required=False)


class ReposicaoEstoqueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = estoque_model.ReposicaoEstoque
        load_instance = True
        fields = ("id", "produto_id", "data_solicitacao", "produto")

    produto_id = fields.Integer(required=False)
    data_solicitacao = fields.Date(required=True)
    produto = fields.Integer(required=False)
