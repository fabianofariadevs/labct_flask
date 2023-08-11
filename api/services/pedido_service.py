from ..models import pedido_model
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria
def cadastrar_pedido(pedido):
    # TODO a função cadastrar_pedido recebe um objeto pedido como argumento e cria uma instância do modelo pedido com os valores do objeto fornecido. Em seguida, adiciona a instância ao banco de dados usando db.session.add() e faz o commit das alterações usando db.session.commit(). Por fim, retorna a instância do pedido cadastrado.
    pedido_bd = pedido_model.Pedido(qtde_pedido=pedido.qtde_pedido, data_pedido=pedido.data_pedido, data_entrega=pedido.data_entrega,
                                    status=pedido.status, obs=pedido.obs, produto_id=pedido.produto_id,
                                    fornecedor_id=pedido.fornecedor_id, filial_pdv=pedido.filial_pdv)

    db.session.add(pedido_bd)
    db.session.commit()
    return pedido_bd

def listar_pedidos():
    #TODO a função listar_pedidos recupera todos os registros da tabela pedido no banco de dados usando pedido_model.pedido.query.all(). Em seguida, retorna uma lista com todos os pedidos encontrados.
    pedidos = pedido_model.Pedido.query.all()
    return pedidos

def listar_pedido_id(id):
    #TODO a função listar_pedido_id recebe um argumento id e recupera o registro da tabela pedido que corresponde ao id fornecido usando pedido_model.pedido.query.filter_by(id=id).first(). Retorna o pedido encontrado ou None se nenhum pedido correspondente for encontrado.
    pedido = pedido_model.Pedido.query.filter_by(id=id).first()

    return pedido

def atualiza_pedido(pedido_anterior, pedido_novo):
    #TODO a função atualiza_pedido recebe dois argumentos, pedido_anterior e pedido_novo, que representam respectivamente o pedido existente a ser atualizado e os novos dados do pedido. Os atributos do pedido_anterior são atualizados com os valores do pedido_novo. Em seguida, as alterações são commitadas no banco de dados usando db.session.commit().
    pedido_anterior.qtde_pedido = pedido_novo.qtde_pedido
    pedido_anterior.data_pedido = pedido_novo.data_pedido
    pedido_anterior.data_entrega = pedido_novo.data_entrega
    # Verifica se pedido_novo.status é uma string 'True' ou 'False'
    # e converte para um valor booleano adequado
    pedido_anterior.status = bool(pedido_novo.status)
    pedido_anterior.obs = pedido_novo.obs
    #pedido_anterior.tipo = pedido_novo.tipo
    pedido_anterior.produto_id = pedido_novo.produto_id
    pedido_anterior.fornecedor_id = pedido_novo.fornecedor_id
    pedido_anterior.filial_pdv = pedido_novo.filial_pdv

    db.session.commit()

def remove_pedido(pedido):
    #TODO a função remove_pedido recebe um argumento pedido que representa o pedido a ser removido. A função remove o pedido do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(pedido)
    db.session.commit()


#TODO service para PEDIDO DE PRODUCAO**
def cadastrar_pedidoprod(pedidoproducao):
    # TODO a função cadastrar_pedido recebe um objeto pedido como argumento e cria uma instância do modelo pedido com os valores do objeto fornecido. Em seguida, adiciona a instância ao banco de dados usando db.session.add() e faz o commit das alterações usando db.session.commit(). Por fim, retorna a instância do pedido cadastrado.
    pedido_bd = pedido_model.PedidoProducao(data_pedido=pedidoproducao.data_pedido, data_entrega=pedidoproducao.data_entrega, qtde_pedido=pedidoproducao.qtde_pedido, status=pedidoproducao.status,
                                    obs=pedidoproducao.obs, receita_id=pedidoproducao.receita_id, filial_pdv=pedidoproducao.filial_pdv)

    db.session.add(pedido_bd)
    db.session.commit()
    return pedido_bd

def listar_pedidosprod():
    #TODO a função listar_pedidos recupera todos os registros da tabela pedido no banco de dados usando pedido_model.pedido.query.all(). Em seguida, retorna uma lista com todos os pedidos encontrados.
    pedidosprod = pedido_model.PedidoProducao.query.all()
    return pedidosprod

def listar_pedidoprod_id(id):
    #TODO a função listar_pedido_id recebe um argumento id e recupera o registro da tabela pedido que corresponde ao id fornecido usando pedido_model.pedido.query.filter_by(id=id).first(). Retorna o pedido encontrado ou None se nenhum pedido correspondente for encontrado.
    pedidoprod = pedido_model.PedidoProducao.query.filter_by(id=id).first()
    return pedidoprod

def atualiza_pedidoprod(pedido_anterior, pedido_novo):
    #TODO a função atualiza_pedido recebe dois argumentos, pedido_anterior e pedido_novo, que representam respectivamente o pedido existente a ser atualizado e os novos dados do pedido. Os atributos do pedido_anterior são atualizados com os valores do pedido_novo. Em seguida, as alterações são commitadas no banco de dados usando db.session.commit().
    pedido_anterior.data_pedido = pedido_novo.data_pedido
    pedido_anterior.data_entrega = pedido_novo.data_entrega
    pedido_anterior.qtde_pedido = pedido_novo.qtde_pedido
    pedido_anterior.status = bool(pedido_novo.status)
    pedido_anterior.obs = pedido_novo.obs
    pedido_anterior.receita_id = pedido_novo.receita_id
    pedido_anterior.filial_pdv = pedido_novo.filial_pdv

    db.session.commit()

def remove_pedidoprod(pedidoprod):
    #TODO a função remove_pedido recebe um argumento pedido que representa o pedido a ser removido. A função remove o pedido do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(pedidoprod)
    db.session.commit()


