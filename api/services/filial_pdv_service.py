from sqlalchemy import func

from ..models import filial_pdv_model
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_filial_pdv(filial):
    filial_bd = filial_pdv_model.Filial(nome=filial.nome, endereco=filial.endereco, bairro=filial.bairro, cidade=filial.cidade, estado=filial.estado,
                                        responsavel=filial.responsavel, whatsapp=filial.whatsapp, cnpj=filial.cnpj, status=filial.status, cadastrado_em=func.now(),
                                        atualizado_em=filial.atualizado_em, cliente=filial.cliente)

    db.session.add(filial_bd)
    db.session.commit()
    return filial_bd

def listar_filial_pdv():
    filial_pdv = filial_pdv_model.Filial.query.all()
    return filial_pdv

def listar_filial_pdv_id(id):
    filial_pdv = filial_pdv_model.Filial.query.filter_by(id=id).first()
    return filial_pdv

def atualiza_filial_pdv(filial_pdv_anterior, filial_pdv_novo):
    filial_pdv_anterior.nome = filial_pdv_novo.nome
    filial_pdv_anterior.endereco = filial_pdv_novo.endereco
    filial_pdv_anterior.bairro = filial_pdv_novo.bairro
    filial_pdv_anterior.cidade = filial_pdv_novo.cidade
    filial_pdv_anterior.estado = filial_pdv_novo.estado
    filial_pdv_anterior.responsavel = filial_pdv_novo.responsavel
    filial_pdv_anterior.whatsapp = filial_pdv_novo.whatsapp
    filial_pdv_anterior.cnpj = filial_pdv_novo.cnpj
    filial_pdv_anterior.status = filial_pdv_novo.status
    filial_pdv_anterior.cadastrado_em = filial_pdv_novo.cadastrado_em
    filial_pdv_anterior.atualizado_em = filial_pdv_novo.atualizado_em
    #filial_pdv_anterior.receitas = filial_pdv_novo.receitas
    #filial_pdv_anterior.pedidos = filial_pdv_novo.pedidos
    filial_pdv_anterior.cliente = filial_pdv_novo.cliente
   # filial_pdv_anterior.pedidosprod = filial_pdv_novo.pedidosprod

    db.session.commit()

def remove_filial_pdv(filial):
    db.session.delete(filial)
    db.session.commit()
