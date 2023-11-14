from api import ma
from ..models import receita_model
from marshmallow import fields
from ..schemas.mix_produto_schema import MixProdutoSchema

#TODO ** Classe ReceitaSchema_Modelo ** este esquema define como os objetos da classe Receita devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class ReceitaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = receita_model.Receita
        load_instance = True
        include_relationships = True # Inclui automaticamente os relacionamentos
        fields = ("id", "descricao_mix", "modo_preparo", "departamento", "rend_kg", "rend_unid", "validade", "status", "cadastrado_em", "atualizado_em",
                  "usuario", "cliente", "mixprodutos", "pedidosprod")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    descricao_mix = fields.String(required=True)
    modo_preparo = fields.String(required=True)
    departamento = fields.String(required=True)
    rend_kg = fields.Float(required=True)
    rend_unid = fields.Float(required=True)
    validade = fields.Integer(required=True)
    status = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)

    usuario = ma.Nested("UsuarioSchema", only=('id', 'nome'))
    cliente = ma.Nested("ClienteSchema", many=False, only=('id', 'nome'))
    mixprodutos = ma.Nested("MixProdutoSchema", many=True, only=('id', 'cod_prod_mix', 'situacao', 'status'))
    pedidosprod = ma.Nested("PedidoProducaoSchema", many=True, exclude=("receitas",))
