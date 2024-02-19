from api import ma
from ..models import estoque_model
from marshmallow import fields

#TODO ** Classe EstoqueSchema_Modelo ** este esquema define como os objetos da classe Estoque devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class EstoqueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = estoque_model.Estoque
        load_instance = True
        include_relationships = True # Inclui automaticamente os relacionamentos
        fields = ("id", "nome", "validade", "valor_ultima_compra", "quantidade_minima", "obs", "quantidade_atual", "status", "cadastro_em", "atualizado_em",
                  "produto", "fornecedor", "cliente", "filiais")

    nome = fields.String(required=False)
    validade = fields.Date(required=True)
    valor_ultima_compra = fields.Float(required=False)
    quantidade_minima = fields.Integer(required=False)
    obs = fields.String(required=False)
    quantidade_atual = fields.Integer(required=False)
    status = fields.Integer(required=False)
    cadastro_em = fields.Date(required=False)
    atualizado_em = fields.Date(required=False)

    produto = ma.Nested("ProdutoMpSchema", only=('id', 'nome'))
    cliente = ma.Nested("ClienteSchema", only=('id', 'nome'))
    filiais = ma.Nested("FilialSchema", only=('id', 'nome'))
    fornecedor = ma.Nested("FornecedorSchema", only=('id', 'nome'))


class ReposicaoEstoqueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = estoque_model.ReposicaoEstoque
        load_instance = True
        fields = ("id", "produto_id", "data_solicitacao", "produto")

    produto_id = fields.Integer(required=False)
    data_solicitacao = fields.Date(required=True)
    produto = fields.Integer(required=False)
