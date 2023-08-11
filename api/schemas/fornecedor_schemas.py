from api import ma
from ..models import fornecedor_model
from marshmallow import fields
from ..models.produtoMp_model import Produto
from ..schemas.produtoMp_schema import ProdutoMpSchema

#TODO ** Classe FornecedorSchema_Modelo ** este esquema define como os objetos da classe Fornecedor devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
#     @author Fabiano Faria

class ProdutoField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return []
        return [produto.id for produto in value]

    def _deserialize(self, value, attr, data, **kwargs):
        from ..models.produtoMp_model import Produto  # Certifique-se de importar corretamente
        if not value:
            return []
        produtos_ids = [int(prod_id) for prod_id in value]
        produtos = Produto.query.filter(Produto.id.in_(produtos_ids)).all()
        return produtos

class FornecedorSchema(ma.SQLAlchemyAutoSchema):
    #produtos = ma.Nested(produtoMp_schema.ProdutoMpSchema, many=True, only=('id', 'nome'))
   # produtos = fields.List(fields.Integer(), required=False)

    class Meta:
        model = fornecedor_model.Fornecedor
        load_instance = True
        fields = ("id", "nome", "descricao", "endereco", "bairro", "cidade", "estado", "telefone", "email",
                  "responsavel", "whatsapp", "cnpj", "status", "cadastrado_em", "atualizado_em", "produtos")

   # produto_id = fields.Integer(required=True)
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
    produtos = ma.List(ma.Nested(ProdutoMpSchema), attribute='produtos', dump_only=True)

    def make_instance(self, data, **kwargs):
        data['produtos'] = [Produto.query.get(produto_id) for produto_id in data.pop('produtos', [])]
        return super().make_instance(data, **kwargs)

