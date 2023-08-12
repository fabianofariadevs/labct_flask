from api import ma
from ..models import receita_model
from marshmallow import fields

#TODO ** Classe ReceitaSchema_Modelo ** este esquema define como os objetos da classe Receita devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class ReceitaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = receita_model.Receita
        load_instance = True
        fields = ("id", "descricao_mix", "modo_preparo", "departamento", "rend_kg", "rend_unid", "validade", "status", "cadastrado_em",
                  "atualizado_em", "produto_id", "filial", "pedidoprod")

    descricao_mix = fields.String(required=True)
    modo_preparo = fields.String(required=True)
    departamento = fields.String(required=True)
    rend_kg = fields.Float(required=True)
    rend_unid = fields.Float(required=True)
    validade = fields.Date(required=True)
    status = fields.Integer(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)
    produto_id = fields.String(required=False)
    filial = fields.String(required=False)
    pedidoprod = fields.String(required=False)


