from api import ma
from ..models import usuario_model
from marshmallow import fields
from ..schemas import cliente_schema

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = usuario_model.Usuario
        load_instance = True
        fields = ("id", "nome", "email", "senha", "is_admin", "status", "cadastrado_em", "atualizado_em", "api_key", "empresa", "cargo")

    id = fields.Integer(primary_key=True, autoincrement=True, nullable=False, dump_only=True)
    nome = fields.String(required=True)
    email = fields.String(required=True)
    senha = fields.String(required=False)
    is_admin = fields.Integer(required=False)
    status = fields.Integer(required=True)
    cadastrado_em = fields.DateTime(required=False)
    atualizado_em = fields.DateTime(required=False)
    api_key = fields.String(required=False)
    empresa = fields.String(required=False)
    #empresa = fields.List(fields.Nested(cliente_schema.ClienteSchema(), only=('id', 'nome')))
    cargo = fields.String(required=False)

