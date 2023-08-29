from sqlalchemy import func

from ..models import cliente_model
from api import db
from datetime import datetime

#TODO * Definição do CRUD_Modelo para Cliente, ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#     @author Fabiano Faria

# ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela Cliente no banco de dados.
def cadastrar_cliente(cliente):
    # TODO a função cadastrar_cliente recebe um objeto cliente como argumento e cria uma instância do modelo Cliente com os valores do objeto fornecido. Em seguida, adiciona a instância ao banco de dados usando db.session.add() e faz o commit das alterações usando db.session.commit(). Por fim, retorna a instância do cliente cadastrado.
    cliente_bd = cliente_model.Cliente(nome=cliente.nome, endereco=cliente.endereco, bairro=cliente.bairro,
                                       cidade=cliente.cidade, estado=cliente.estado, telefone=cliente.telefone,
                                       email=cliente.email, responsavel=cliente.responsavel, whatsapp=cliente.whatsapp,
                                       cnpj=cliente.cnpj, status=cliente.status, cadastrado_em=func.now(),
                                       atualizado_em=cliente.atualizado_em, filial_id=cliente.filial_id)

    db.session.add(cliente_bd)
    db.session.commit()
    return cliente_bd

def listar_clientes():
    #TODO a função listar_clientes recupera todos os registros da tabela Cliente no banco de dados usando cliente_model.Cliente.query.all(). Em seguida, retorna uma lista com todos os clientes encontrados.
    clientes = cliente_model.Cliente.query.all()
    return clientes

def listar_cliente_id(id):
    #TODO a função listar_cliente_id recebe um argumento id e recupera o registro da tabela Cliente que corresponde ao id fornecido usando cliente_model.Cliente.query.filter_by(id=id).first(). Retorna o cliente encontrado ou None se nenhum cliente correspondente for encontrado.
    cliente = cliente_model.Cliente.query.filter_by(id=id).first()
    return cliente

def atualiza_cliente(cliente_anterior, cliente_novo):
    #TODO a função atualiza_cliente recebe dois argumentos, cliente_anterior e cliente_novo, que representam respectivamente o cliente existente a ser atualizado e os novos dados do cliente. Os atributos do cliente_anterior são atualizados com os valores do cliente_novo. Em seguida, as alterações são commitadas no banco de dados usando db.session.commit().
    cliente_anterior.nome = cliente_novo.nome
    cliente_anterior.endereco = cliente_novo.endereco
    cliente_anterior.bairro = cliente_novo.bairro
    cliente_anterior.cidade = cliente_novo.cidade
    cliente_anterior.estado = cliente_novo.estado
    cliente_anterior.telefone = cliente_novo.telefone
    cliente_anterior.email = cliente_novo.email
    cliente_anterior.responsavel = cliente_novo.responsavel
    cliente_anterior.whatsapp = cliente_novo.whatsapp
    cliente_anterior.cnpj = cliente_novo.cnpj
    cliente_anterior.status = cliente_novo.status
    cliente_anterior.cadastrado_em = cliente_novo.cadastrado_em
    #cliente_anterior.atualizado_em = datetime.now()
    cliente_anterior.atualizado_em = cliente_novo.atualizado_em
    cliente_anterior.filial_id = cliente_novo.filial_id
    db.session.commit()

def deletar_cliente(cliente):
    #TODO a função remove_cliente recebe um argumento cliente que representa o cliente a ser removido. A função remove o cliente do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(cliente)
    db.session.commit()


