from api import ma
from ..models import filial_pdv_model
from marshmallow import fields


#TODO ** Classe FilialSchema_Modelo ** este esquema define como os objetos da classe Filial devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class FilialSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = filial_pdv_model.Filial
        load_instance = True
        fields = ("id", "nome", "endereco", "bairro", "cidade", "estado", "responsavel", "whatsapp", "cnpj", "status", "cadastrado_em", "atualizado_em",
                  "cliente", "estoques", "mixprodutos", "pedidosprod", "producoes")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    nome = fields.String(required=True)
    endereco = fields.String(required=True)
    bairro = fields.String(required=True)
    cidade = fields.String(required=True)
    estado = fields.String(required=True)
    responsavel = fields.String(required=True)
    whatsapp = fields.String(required=True)
    cnpj = fields.String(required=True)
    status = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)

    estoques = ma.Nested("EstoqueSchema", many=True, exclude=("filiais",))
    mixprodutos = ma.Nested("MixProdutoSchema", many=True, exclude=("filiais",))
    pedidosprod = ma.Nested("PedidoProducaoSchema", many=True, exclude=("filiais",))
    cliente = ma.Nested("ClienteSchema", many=False, only=('id', 'nome'))
    producoes = ma.Nested("ProducaoSchema", many=False, exclude=("filial",))

