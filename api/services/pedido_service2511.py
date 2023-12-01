from api import db
from sqlalchemy import func
from ..models import pedido_model, fornecedor_model, produtoMp_model
from ..services import cliente_service, fornecedor_service, produtoMp_service
from datetime import datetime, date


#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_pedidoc(form_data):
    if isinstance(form_data, dict):
        data_entrega = form_data.get('data_entrega')
        if isinstance(data_entrega, str):
            form_data['data_entrega'] = datetime.strptime(data_entrega, '%Y-%m-%d').date()
        atualizado_em = form_data.get('atualizado_em')
        if isinstance(atualizado_em, str):
            form_data['atualizado_em'] = datetime.strptime(atualizado_em, '%Y-%m-%d').date()

        pedido_bd = pedido_model.Pedido(
            qtde_pedido=form_data.get('qtde_pedido'),
            data_pedido=func.now(),
            data_entrega=form_data.get('data_entrega'),
            status=form_data.get('status'),
            obs=form_data.get('obs'),
            cadastrado_em=func.now(),
            atualizado_em=form_data.get('atualizado_em'),
            clientes=cliente_service.listar_cliente_id(form_data.get('clientes')),
            fornecedores=fornecedor_service.listar_fornecedor_id(form_data.get('fornecedores')),
            produtos=produtoMp_service.listar_produto_id(form_data.get('produtos'))
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

def atualiza_pedidoc(pedido_anterior, pedido_novo, form_data, qtde):
    #TODO a função atualiza_pedido recebe dois argumentos, pedido_anterior e pedido_novo, que representam respectivamente o pedido existente a ser atualizado e os novos dados do pedido. Os atributos do pedido_anterior são atualizados com os valores do pedido_novo. Em seguida, as alterações são commitadas no banco de dados usando db.session.commit().
    if pedido_anterior:
        pedido_anterior.qtde_pedido = int(qtde)
        pedido_anterior.data_pedido = func.now()
        pedido_anterior.data_entrega = form_data.data_entrega.data
        pedido_anterior.status = form_data.status.data
        pedido_anterior.obs = form_data.obs.data
        # Limpe e estenda a relação de 1 para muitos com Produto
        pedido_anterior.produtos.clear()
        if isinstance(form_data.produtos.data, (list, set, tuple)):
            for produto_id in form_data.produtos.data:
                produto = produtoMp_model.Produto.query.get(produto_id)
                if produto:
                    pedido_anterior.produtos.append(produto)

        # Atualize a relação de 1 para 1 com Fornecedor
        # Certifique-se de que form_data.fornecedores.data seja um objeto Fornecedor
        fornecedor_novo = form_data.fornecedores.data
        if isinstance(fornecedor_novo, int):
            fornecedor_novo = fornecedor_model.Fornecedor.query.get(fornecedor_novo)
        pedido_anterior.fornecedores = fornecedor_novo
      #  if isinstance(form_data.fornecedores.data, (list, set, tuple)):
       #     for fornecedor_id in form_data.fornecedores.data:
      #          fornecedor = fornecedor_model.Fornecedor.query.get(fornecedor_id)
       #         if fornecedor:
      #              pedido_anterior.fornecedores.append(fornecedor)

        # Atualize a relação de 1 para 1 com Cliente
        cliente = cliente_service.listar_cliente_id(form_data)
        pedido_anterior.clientes = cliente

      #  pedido_anterior.cadastrado_em = pedido_novo.cadastrado_em
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
        if isinstance(qtde_pedido, str):
            pedidoprod['qtde_pedido'] = int(qtde_pedido)

        situacao = pedidoprod.get('situacao')
        if isinstance(situacao, str):
            pedidoprod['situacao'] = int(situacao)

        status = pedidoprod.get('status')
        if isinstance(status, str):
            pedidoprod['status'] = int(status)

        obs = pedidoprod.get('obs')
        if isinstance(obs, str):
            pedidoprod['obs'] = obs

        cadastrado_em = pedidoprod.get('cadastrado_em')
        if isinstance(cadastrado_em, str):
            pedidoprod['cadastrado_em'] = datetime.strptime(cadastrado_em, '%Y-%m-%d').date()

        atualizado_em = pedidoprod.get('atualizado_em')
        if isinstance(atualizado_em, str):
            pedidoprod['atualizado_em'] = datetime.strptime(atualizado_em, '%Y-%m-%d').date()

        mixprodutos = pedidoprod.get('mixprodutos')
        if isinstance(mixprodutos, str):
            pedidoprod['mixprodutos'] = mixprodutos

        filiais = pedidoprod.get('filiais')
        if isinstance(filiais, str):
            pedidoprod['filiais'] = filiais

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

