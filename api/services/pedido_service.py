from api import db
from sqlalchemy import func
from ..models import pedido_model, fornecedor_model, cliente_model, produtoMp_model
from datetime import datetime, date



#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_pedido(pedido):
    if isinstance(pedido, dict):
        data_entrega = pedido.get('data_entrega')
        if isinstance(data_entrega, str):
            pedido['data_entrega'] = datetime.strptime(data_entrega, '%Y-%m-%d').date()
        atualizado_em = pedido.get('atualizado_em')
        if isinstance(atualizado_em, str):
            pedido['atualizado_em'] = datetime.strptime(atualizado_em, '%Y-%m-%d').date()

        pedido_bd = pedido_model.Pedido(
            qtde_pedido=pedido['qtde_pedido'],
            data_pedido=func.now(),
            data_entrega=pedido['data_entrega'],
            status=pedido['status'],
            obs=pedido['obs'],
            cadastrado_em=func.now(),
            atualizado_em=atualizado_em,
            clientes=pedido['clientes'],
            fornecedores=pedido['fornecedores'],
            produtos=pedido['produtos']
        )
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
    if pedido_anterior:
        pedido_anterior.qtde_pedido = pedido_novo.qtde_pedido
        pedido_anterior.data_pedido = pedido_novo.data_pedido
        pedido_anterior.data_entrega = pedido_novo.data_entrega
        pedido_anterior.status = pedido_novo.status
        pedido_anterior.obs = pedido_novo.obs

        # Limpe e estenda a relação de 1 para muitos com Produto
        pedido_anterior.produtos.clear()
        produtos_novos = [produtoMp_model.Produto.query.get(produto.id) for produto in pedido_novo.produtos]
        pedido_anterior.produtos.extend(produtos_novos)

        # Atualize a relação de 1 para 1 com Fornecedor
        pedido_anterior.fornecedores = fornecedor_model.Fornecedor.query.get(pedido_novo.fornecedores)

        # Atualize a relação de 1 para 1 com Cliente
        pedido_anterior.clientes = cliente_model.Cliente.query.get(pedido_novo.clientes)

        pedido_anterior.cadastrado_em = pedido_novo.cadastrado_em
        pedido_anterior.atualizado_em = func.now()

        db.session.add(pedido_anterior)
        db.session.commit()
    else:
        return None


def remove_pedido(pedido):
    #TODO a função remove_pedido recebe um argumento pedido que representa o pedido a ser removido. A função remove o pedido do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(pedido)
    db.session.commit()


#TODO service para PEDIDO DE PRODUCAO**
def cadastrar_pedidoprod(pedidoprod):
    if isinstance(pedidoprod, dict):
        data_entrega = pedidoprod.get('data_entrega')
        if isinstance(data_entrega, str):
            pedidoprod['data_entrega'] = datetime.strptime(data_entrega, '%Y-%m-%d').date()

        qtde_pedido = pedidoprod.get('qtde_pedido')
        status = pedidoprod.get('status')
        obs = pedidoprod.get('obs')
        atualizado_em = pedidoprod.get('atualizado_em')
        if isinstance(atualizado_em, str):
            pedidoprod['atualizado_em'] = datetime.strptime(atualizado_em, '%Y-%m-%d').date()
        mixprodutos = pedidoprod.get('mixprodutos')
        filiais = pedidoprod.get('filiais')
        pedidoprod_bd = pedido_model.PedidoProducao(data_pedido=func.now(), data_entrega=pedidoprod['data_entrega'],
                                                    qtde_pedido=pedidoprod['qtde_pedido'], status=pedidoprod['status'], obs=pedidoprod['obs'],
                                                    cadastrado_em=func.now(), atualizado_em=atualizado_em)

        db.session.add(pedidoprod_bd)
        db.session.commit()
        return pedidoprod_bd

def cadastrar_pedidoprod2(pedidoprod):
    # TODO a função cadastrar_pedido recebe um objeto pedido como argumento e cria uma instância do modelo pedido com os valores do objeto fornecido. Em seguida, adiciona a instância ao banco de dados usando db.session.add() e faz o commit das alterações usando db.session.commit(). Por fim, retorna a instância do pedido cadastrado.
    # Cria uma instância do modelo Pedido com os valores fornecidos no objeto 'pedido'
    pedidoprod_bd = pedido_model.PedidoProducao(data_pedido=func.now(), data_entrega=pedidoprod.data_entrega,
                                                qtde_pedido=pedidoprod.qtde_pedido, status=pedidoprod.status, obs=pedidoprod.obs,
                                                cadastrado_em=func.now(), atualizado_em=pedidoprod.atualizado_em)

    pedidoprod_bd.mixprodutos = pedidoprod['mixprodutos']
    pedidoprod_bd.filiais = pedidoprod['filiais']

    db.session.add(pedidoprod_bd)
    db.session.commit()
    return pedidoprod_bd


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
    pedido_anterior.mixprodutos = pedido_novo.mixprodutos
    pedido_anterior.filiais = pedido_novo.filiais
    pedido_anterior.cadastrado_em = pedido_novo.cadastrado_em
    pedido_anterior.atualizado_em = pedido_novo.atualizado_em

    db.session.commit()

def remove_pedidoprod(pedidoprod):
    #TODO a função remove_pedido recebe um argumento pedido que representa o pedido a ser removido. A função remove o pedido do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(pedidoprod)
    db.session.commit()

