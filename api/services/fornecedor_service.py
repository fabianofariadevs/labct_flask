from sqlalchemy import func
from ..models import fornecedor_model
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_fornecedor(fornecedor):
    fornecedor_bd = fornecedor_model.Fornecedor(descricao=fornecedor.descricao, nome=fornecedor.nome, cnpj=fornecedor.cnpj,
                                                endereco=fornecedor.endereco, bairro=fornecedor.bairro, cidade=fornecedor.cidade, estado=fornecedor.estado,
                                                email=fornecedor.email, telefone=fornecedor.telefone, responsavel=fornecedor.responsavel, status=fornecedor.status,
                                                whatsapp=fornecedor.whatsapp, cadastrado_em=func.now(), atualizado_em=fornecedor.atualizado_em)

    db.session.add(fornecedor_bd)
    db.session.commit()
    return fornecedor_bd

def listar_fornecedores():
    fornecedor = fornecedor_model.Fornecedor.query.all()
    return fornecedor

def listar_fornecedor_id(id):
    fornecedor = fornecedor_model.Fornecedor.query.filter_by(id=id).first()
    return fornecedor

def atualiza_fornecedor(fornecedor_anterior, fornecedor_novo):
    fornecedor_anterior.descricao = fornecedor_novo.descricao
    fornecedor_anterior.nome = fornecedor_novo.nome
    fornecedor_anterior.cnpj = fornecedor_novo.cnpj
    fornecedor_anterior.endereco = fornecedor_novo.endereco
    fornecedor_anterior.bairro = fornecedor_novo.bairro
    fornecedor_anterior.cidade = fornecedor_novo.cidade
    fornecedor_anterior.estado = fornecedor_novo.estado
    fornecedor_anterior.email = fornecedor_novo.email
    fornecedor_anterior.telefone = fornecedor_novo.telefone
    fornecedor_anterior.responsavel = fornecedor_novo.responsavel
    fornecedor_anterior.status = fornecedor_novo.status
    fornecedor_anterior.whatsapp = fornecedor_novo.whatsapp
    fornecedor_anterior.cadastrado_em = fornecedor_novo.cadastrado_em
    fornecedor_anterior.atualizado_em = fornecedor_novo.atualizado_em

    db.session.commit()

def remove_fornecedor(fornecedor):
    db.session.delete(fornecedor)
    db.session.commit()
