from api import ma
from ..models import fornecedor_model
from marshmallow import fields
from ..models.produtoMp_model import Produto
from ..schemas.produtoMp_schema import ProdutoMpSchema

#TODO ** Classe FornecedorSchema_Modelo ** este esquema define como os objetos da classe Fornecedor devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class FornecedorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = fornecedor_model.Fornecedor
        load_instance = True
        fields = ("id", "nome", "descricao", "endereco", "bairro", "cidade", "estado", "telefone", "email",
                  "responsavel", "whatsapp", "cnpj", "status", "cadastrado_em", "atualizado_em")

   # produto_id = fields.Integer(required=True)
    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    endereco = fields.String(required=True)
    bairro = fields.String(required=True)
    cidade = fields.String(required=True)
    estado = fields.String(required=True)
    telefone = fields.String(required=True)
    email = fields.String(required=True)
    responsavel = fields.String(required=True)
    whatsapp = fields.String(required=False)
    cnpj = fields.String(required=True)
    status = fields.Integer(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)
    #produtos = fields.String(required=True)
   # produtos = ma.List(ma.Nested(ProdutoMpSchema), attribute='produtos', dump_only=True)
