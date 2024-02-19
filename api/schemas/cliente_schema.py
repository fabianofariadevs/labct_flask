from api import ma, db
from ..models import cliente_model, usuario_model
from marshmallow import fields

#TODO ** Classe Clienteschema_odelo ** este esquema define como os objetos da classe Cliente devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelo
#     @author Fabiano Faria
class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = cliente_model.Cliente
        load_instance = True # TODO Define se o esquema Cliente deve carregar uma instância do modelo ao fazer a desserialização. Nesse caso, está definido como True.
        include_relationships = True
        fields = ("id", "nome", "endereco", "bairro", "cidade", "estado", "telefone", "email", "responsavel", "whatsapp", "cnpj", "status", "cadastrado_em", "atualizado_em",
                  "filiais", "receitas", "pedido_compra", "pedidosprod", "usuarios", "estoques", "funcoes")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    nome = fields.String(required=True)
    endereco = fields.String(required=True)
    bairro = fields.String(required=True)
    cidade = fields.String(required=True)
    estado = fields.String(required=True)
    telefone = fields.String(required=True)
    email = fields.String(required=True)
    responsavel = fields.String(required=True)
    whatsapp = fields.String(required=True)
    cnpj = fields.String(required=True)
    status = fields.Integer(required=False)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)

    filiais = ma.Nested("FilialSchema", many=False, exclude=("cliente",), only=("id", "nome", "bairro", "status"))
    receitas = ma.Nested("ReceitaSchema", many=False, only=("id", "descricao_mix", "modo_preparo", "departamento", "rend_kg", "rend_unid", "validade", "status", "cadastrado_em", "atualizado_em"))
    pedido_compra = ma.Nested("PedidoSchema", many=False, exclude=("clientes",))
    pedidosprod = ma.Nested("PedidoProducaoSchema", many=True, exclude=("cliente",), only=("id", "data_pedido", "data_entrega", "qtde_pedido", "status", "obs", "cadastrado_em", "atualizado_em"))
    usuarios = ma.Nested("UsuarioSchema", many=True, exclude=("cliente",))
    estoques = ma.Nested("EstoqueSchema", many=True, exclude=("cliente",))
    funcoes = ma.Nested("FuncaoSchema", many=False, exclude=("usuarios",))






