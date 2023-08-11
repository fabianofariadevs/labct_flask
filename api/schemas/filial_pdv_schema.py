from api import ma
from ..models import filial_pdv_model
from marshmallow import fields
from ..schemas import cliente_schema, receita_schema

#TODO ** Classe FilialSchema_Modelo ** este esquema define como os objetos da classe Filial devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class FilialSchema(ma.SQLAlchemyAutoSchema):
    receitas = ma.Nested(receita_schema.ReceitaSchema, many=True, only=('id', 'descricao_mix'))

    class Meta:
        model = filial_pdv_model.Filial
        load_instance = True
        fields = ("id", "nome", "endereco", "bairro", "cidade", "estado", "responsavel", "whatsapp", "cnpj", "status", "cadastrado_em", "atualizado_em", "cliente")

    nome = fields.String(required=True)
    endereco = fields.String(required=True)
    bairro = fields.String(required=True)
    cidade = fields.String(required=True)
    estado = fields.String(required=True)
    responsavel = fields.String(required=True)
    whatsapp = fields.String(required=True)
    cnpj = fields.String(required=True)
    status = fields.Integer(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)
    cliente = fields.String(required=False)
   # pedidos = fields.String(required=False)
   # pedidosprod = fields.String(required=False)
    #clientes = fields.List(fields.Nested(cliente_schema.ClienteSchema(), only=('id', 'nome')))



