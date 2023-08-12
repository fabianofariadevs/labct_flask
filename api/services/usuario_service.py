from ..models import usuario_model
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_usuario(usuario):
    usuario_bd = usuario_model.Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha, empresa=usuario.empresa, is_admin=usuario.is_admin, status=usuario.status, cadastrado_em=usuario.cadastrado_em, atualizado_em=usuario.atualizado_em, api_key=usuario.api_key, cargo=usuario.cargo)
    usuario_bd.encriptar_senha()
    db.session.add(usuario_bd)
    db.session.commit()
    return usuario_bd

def listar_usuario_email(email):
    usuarioemail = usuario_model.Usuario.query.filter_by(email=email).first()
    return usuarioemail

def listar_usuario_id(id):
    usuario = usuario_model.Usuario.query.filter_by(id=id).first()
    return usuario

def listar_usuarios():
    #TODO a função listar_usuarios recupera todos os registros da tabela Usuarios no banco de dados usando usuario_model.Usuario.query.all(). Em seguida, retorna uma lista com todos os usuarios encontrados.
    usuarios = usuario_model.Usuario.query.all()
#  print("Usuarios retornados:", usuarios)
    return usuarios

def atualizar_usuario(usuario_anterior, usuario_novo):
    usuario_anterior.nome = usuario_novo.nome
    usuario_anterior.email = usuario_novo.email
    usuario_anterior.senha = usuario_novo.senha
    usuario_anterior.is_admin = usuario_novo.is_admin
    usuario_anterior.status = bool(usuario_novo.status)
    usuario_anterior.empresa = usuario_novo.empresa
    usuario_anterior.cadastrado_em = usuario_novo.cadastrado_em
    usuario_anterior.atualizado_em = usuario_novo.atualizado_em

    db.session.commit()

