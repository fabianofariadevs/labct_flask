from sqlalchemy import func
from ..models import pedido_model, receita_model, produtoMp_model, estoque_model
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria
def cadastrar_pedido(pedido):
    # TODO a função cadastrar_pedido recebe um objeto pedido como argumento e cria uma instância do modelo pedido com os valores do objeto fornecido. Em seguida, adiciona a instância ao banco de dados usando db.session.add() e faz o commit das alterações usando db.session.commit(). Por fim, retorna a instância do pedido cadastrado.

    pedido_bd = pedido_model.Pedido(qtde_pedido=pedido.qtde_pedido, data_pedido=func.now(), data_entrega=pedido.data_entrega,
                                    status=pedido.status, obs=pedido.obs, cadastrado_em=func.now(), atualizado_em=pedido.atualizado_em, produto_id=pedido.produto_id,
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
    pedido_anterior.status = pedido_novo.status
    pedido_anterior.obs = pedido_novo.obs
    pedido_anterior.produto_id = pedido_novo.produto_id
    pedido_anterior.fornecedor_id = pedido_novo.fornecedor_id
    pedido_anterior.filial_pdv = pedido_novo.filial_pdv
    pedido_anterior.cadastrado_em = pedido_novo.cadastrado_em
    pedido_anterior.atualizado_em = pedido_novo.atualizado_em

    db.session.commit()

def remove_pedido(pedido):
    #TODO a função remove_pedido recebe um argumento pedido que representa o pedido a ser removido. A função remove o pedido do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(pedido)
    db.session.commit()


#TODO service para PEDIDO DE PRODUCAO**
def cadastrar_pedidoprod(pedidoproducao):
    receita = receita_model.Receita.query.get(pedidoproducao.receita_id)

    # Verifique se há estoque suficiente antes de criar o pedido
    for item in receita.produtos:
        produto = produtoMp_model.Produto.query.get(item.id)
        estoque = estoque_model.Estoque.query.filter_by(produto_id=produto.id).first()

        if estoque and estoque.quantidade_atual < (item.quantidade + produto.estoque_minimo):
            raise ValueError(f"Estoque insuficiente para {produto.nome}")

    # TODO a função cadastrar_pedido recebe um objeto pedido como argumento e cria uma instância do modelo pedido com os valores do objeto fornecido. Em seguida, adiciona a instância ao banco de dados usando db.session.add() e faz o commit das alterações usando db.session.commit(). Por fim, retorna a instância do pedido cadastrado.
    pedido_bd = pedido_model.PedidoProducao(data_pedido=func.now(), data_entrega=pedidoproducao.data_entrega, qtde_pedido=pedidoproducao.qtde_pedido,
                                            status=pedidoproducao.status, obs=pedidoproducao.obs, receita_id=pedidoproducao.receita_id, filial_pdv=pedidoproducao.filial_pdv,
                                            cadastrado_em=func.now(), atualizado_em=pedidoproducao.atualizado_em, quantidade=pedidoproducao.quantidade, produto_id=pedidoproducao.produto_id)

    db.session.add(pedido_bd)
    db.session.commit()

    # Atualize o estoque após a criação do pedido
    for item in receita.produtos:
        produto = produtoMp_model.Produto.query.get(item.id)
        estoque = estoque_model.Estoque.query.filter_by(produto_id=produto.id).first()

        if estoque:
            estoque.quantidade_atual -= item.quantidade
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
    pedido_anterior.status = pedido_novo.status
    pedido_anterior.obs = pedido_novo.obs
    pedido_anterior.receita_id = pedido_novo.receita_id
    pedido_anterior.filial_pdv = pedido_novo.filial_pdv
    pedido_anterior.cadastrado_em = pedido_novo.cadastrado_em
    pedido_anterior.atualizado_em = pedido_novo.atualizado_em

    db.session.commit()

def remove_pedidoprod(pedidoprod):
    #TODO a função remove_pedido recebe um argumento pedido que representa o pedido a ser removido. A função remove o pedido do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(pedidoprod)
    db.session.commit()


def criar_pedido_producao(data_entrega, qtde_pedido, receita_id, filial_pdv):
    receita = receita_model.Receita.query.get(receita_id)

    # Verifique se há estoque suficiente antes de criar o pedido
    for item in receita.produtos:
        produto = produtoMp_model.Produto.query.get(item.id)
        estoque = estoque_model.Estoque.query.filter_by(produto_id=produto.id).first()

        if estoque and estoque.quantidade_atual < (item.quantidade + produto.estoque_minimo):
            raise ValueError(f"Estoque insuficiente para {produto.nome}")

    pedido_producao = pedido_model.PedidoProducao(data_entrega=data_entrega, qtde_pedido=qtde_pedido,
                                                  receita=receita, filial_pdv=filial_pdv)
    db.session.add(pedido_producao)
    db.session.commit()

    # Atualize o estoque após a criação do pedido
    for item in receita.produtos:
        produto = produtoMp_model.Produto.query.get(item.id)
        estoque = estoque_model.Estoque.query.filter_by(produto_id=produto.id).first()

        if estoque:
            estoque.quantidade_atual -= item.quantidade
            db.session.commit()

    return pedido_producao
