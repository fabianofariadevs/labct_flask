from api import ma
from ..models import cliente_model, usuario_model
from marshmallow import fields


#TODO ** Classe Clienteschema_odelo ** este esquema define como os objetos da classe Cliente devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelo
#     @author Fabiano Faria

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    # TODO Especifica o modelo associado ao esquema, que é cliente_model.Cliente

    class Meta:
        model = cliente_model.Cliente
        load_instance = True  # TODO Define se o esquema Cliente deve carregar uma instância do modelo ao fazer a desserialização. Nesse caso, está definido como True.
        # Uma tupla que especifica quais os campos do modelo devem ser serializados/desserializados. Aqui, são listados vários campos do modelo Cliente.
        fields = ("id", "nome", "endereco", "bairro", "cidade", "estado", "telefone", "email", "responsavel", "whatsapp", "cnpj", "status", "cadastrado_em", "atualizado_em", "filial_id")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    nome = fields.String(required=True)
    endereco = fields.String(required=True)
    bairro = fields.String(required=True)
    cidade = fields.String(required=True)
    estado = fields.String(required=True)
    telefone = fields.String(required=True)
    email = fields.String(required=True)
    responsavel = fields.String(required=True)
    whatsapp = fields.String(required=False)
    cnpj = fields.String(required=False)
    status = fields.Integer(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)
    filial_id = fields.String(required=False)
    #filial = fields.List(fields.Nested(usuario_schema.UsuarioSchema(), only=('id', 'nome')))
    #_links = fields.Dict(dump_only=True)

class FuncaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = usuario_model.Funcao
        load_instance = True
        fields = ("id", "nome", "usuarios")
        many = True
        unknown = 'EXCLUDE'

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    nome = fields.String(required=True)
    usuarios = fields.String(required=False)





