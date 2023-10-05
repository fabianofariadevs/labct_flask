from api import ma
from ..models import receita_model, filial_pdv_model
from ..schemas.produtoMp_schema import ProdutoMpSchema
from marshmallow import fields

#TODO ** Classe ReceitaSchema_Modelo ** este esquema define como os objetos da classe Receita devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class ReceitaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = receita_model.Receita
        load_instance = True
        fields = ("id", "descricao_mix", "modo_preparo", "departamento", "rend_kg", "rend_unid", "validade", "status", "cadastrado_em", "atualizado_em",
                  "quantidades", "filiais", "clientes", "produtos", "pedidosprod")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    descricao_mix = fields.String(required=True)
    modo_preparo = fields.String(required=True)
    departamento = fields.String(required=True)
    rend_kg = fields.Float(required=True)
    rend_unid = fields.Float(required=True)
    validade = fields.String(required=True)
    status = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)
    quantidades = fields.Float(required=False)
    filiais = fields.String(required=False)
    clientes = fields.String(required=False)
    produtos = fields.String(required=False)
    pedidosprod = fields.String(required=False)
    usuario = fields.Integer(required=False)
   # pedidosprod = fields.Nested("PedidoProducao", many=True, exclude=("receitas",))



