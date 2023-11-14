from sqlalchemy import func
from ..models import usuario_model
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_usuario(usuario):
    usuario_bd = usuario_model.Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha,
                                       is_admin=usuario.is_admin, status=usuario.status, cadastrado_em=func.now(),
                                       atualizado_em=usuario.atualizado_em, api_key=usuario.api_key,
                                       )
    usuario_bd.cliente = usuario.cliente
    usuario_bd.funcao = usuario.funcao

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
    usuario_anterior.empresa = usuario_novo.empresa
    usuario_anterior.is_admin = usuario_novo.is_admin
    usuario_anterior.cargo = usuario_novo.cargo
    usuario_anterior.status = usuario_novo.status
    usuario_anterior.cadastrado_em = usuario_novo.cadastrado_em
    usuario_anterior.atualizado_em = usuario_novo.atualizado_em

    db.session.commit()

def deletar_usuario(usuario):
    #TODO a função deletar_usuario recebe um argumento usuario que representa o usuario a ser removido. A função remove o usuario do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(usuario)
    db.session.commit()