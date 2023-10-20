from api import ma
from ..models import filial_pdv_model
from marshmallow import fields
from ..schemas.estoque_schema import EstoqueSchema
from ..schemas.cliente_schema import ClienteSchema
from ..schemas.pedido_schemas import PedidoProducaoSchema


#TODO ** Classe FilialSchema_Modelo ** este esquema define como os objetos da classe Filial devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class FilialSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = filial_pdv_model.Filial
        load_instance = True
        fields = ("id", "nome", "endereco", "bairro", "cidade", "estado", "responsavel", "whatsapp", "cnpj", "status", "cadastrado_em", "atualizado_em",
                  "cliente")

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

   # estoques_filial = fields.String(required=False)
   # mixprodutos = fields.String(required=False)
    cliente = fields.Integer(required=False)
    #pedidosprod = fields.String(required=False)


