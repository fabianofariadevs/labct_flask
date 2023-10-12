from api import ma
from ..models import receita_model
from ..schemas import filial_pdv_schema, cliente_schema, receita_schema
from marshmallow import fields

#TODO ** Classe ReceitaSchema_Modelo ** este esquema define como os objetos da classe Receita devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class ReceitaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = receita_model.Receita
        load_instance = True
        fields = ("id", "descricao_mix", "modo_preparo", "departamento", "rend_kg", "rend_unid", "validade", "status", "cadastrado_em", "atualizado_em",
                  "clientes", "ingredientes", "pedidosprod", "usuario")

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

    usuario = fields.Integer(required=False)
    clientes = fields.String(required=False)
    ingredientes = fields.Nested("IngredientesSchema", many=True, exclude=("receita",))
    pedidosprod = fields.String(required=False)


class IngredientesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = receita_model.Ingredientes
        load_instance = True
        fields = ("id", "nome", "quantidade", "unidade", "receita_id", "receita")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    nome = fields.String(required=True)
    quantidade = fields.Float(required=True)
    unidade = fields.String(required=True)
    receita_id = fields.Integer(required=True)
    receita = fields.Nested("ReceitaSchema", only=('id', 'descricao_mix'))

