from api import ma
from ..models import usuario_model
from marshmallow import fields
from ..schemas import cliente_schema

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = usuario_model.Usuario
        load_instance = True
        include_relationships = True
        fields = ("id", "nome", "email", "senha", "is_admin", "status", "cadastrado_em", "atualizado_em", "api_key",
                  "cliente", "funcao", "producoes")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    nome = fields.String(required=True)
    email = fields.String(required=True)
    senha = fields.String(required=False)
    is_admin = fields.Integer(required=False)
    status = fields.Integer(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)
    api_key = fields.String(required=False)

    cliente = ma.Nested(cliente_schema.ClienteSchema, exclude=("usuarios",), load_only=True)
    funcao = ma.Nested("FuncaoSchema", many=False, exclude=("usuarios",), load_only=True, only=("id", "nome"))
    producoes = ma.Nested("ProducaoSchema", many=False, exclude=("usuario",), load_only=True)

class FuncaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = usuario_model.Funcao
        load_instance = True
        fields = ("id", "nome", "cadastrado_em", "atualizado_em",
                  "usuarios", "cliente")
        many = True
        unknown = 'EXCLUDE'

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    nome = fields.String(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)
    cliente = ma.Nested(cliente_schema.ClienteSchema, exclude=("usuarios",), load_only=True)
    usuarios = ma.Nested(UsuarioSchema, exclude=("cliente",), load_only=True)

