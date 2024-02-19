from api import db
from sqlalchemy import func
from ..models import pedido_model, fornecedor_model, produtoMp_model, cliente_model
from ..services import cliente_service, fornecedor_service, produtoMp_service, filial_pdv_service, mix_produto_service
from datetime import datetime, date
from ..models.mix_produto_model import MixProduto
from ..models.filial_pdv_model import Filial

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_pedidoc(form_data):
    try:
        # Convertendo strings de datas para objetos datetime
        form_data['data_entrega'] = datetime.strptime(form_data['data_entrega'], '%Y-%m-%d').date()
        # Certifique se o ID correspondem a instâncias existentes
        produto = produtoMp_service.listar_produto_id(form_data['produtos'])
        fornecedor = fornecedor_service.listar_fornecedor_id(form_data['fornecedores'])
        cliente = cliente_service.listar_cliente_id(form_data['clientes'])

        if not (produto and fornecedor and cliente):
            raise ValueError("Um ou mais produtos não foram encontrados.")

        pedido_bd = pedido_model.Pedido(
            qtde_pedido=form_data['qtde_pedido'],
            data_pedido=func.now(),
            data_entrega=form_data['data_entrega'],
            status=form_data['status'],
            obs=form_data['obs'],
            cadastrado_em=func.now(),
            produtos=[produto],  # Adicionando o produto à lista de produtos
            fornecedores=[fornecedor],  # Adicionando o fornecedor à lista de fornecedores
            clientes=[cliente]  # Adicionando o cliente à lista de clientes
        )
        db.session.add(pedido_bd)
        db.session.commit()
        return pedido_bd
    except Exception as e:
        raise ValueError(str(e))

def listar_pedidos():
    #TODO a função listar_pedidos recupera todos os registros da tabela pedido no banco de dados usando pedido_model.pedido.query.all(). Em seguida, retorna uma lista com todos os pedidos encontrados.
    pedidos = pedido_model.Pedido.query.all()
    return pedidos

def listar_pedido_id(id):
    #TODO a função listar_pedido_id recebe um argumento id e recupera o registro da tabela pedido que corresponde ao id fornecido usando pedido_model.pedido.query.filter_by(id=id).first(). Retorna o pedido encontrado ou None se nenhum pedido correspondente for encontrado.
    pedido = pedido_model.Pedido.query.filter_by(id=id).first()

    return pedido

def atualiza_pedidoc(pedido, form_data, form):
    try:
        # Atualizar campos simples do Pedido
        pedido.qtde_pedido = form_data['qtde_pedido']
        pedido.data_entrega = datetime.strptime(form_data['data_entrega'], '%Y-%m-%d').date()
        pedido.status = form_data['status']
        pedido.obs = form_data['obs']
        pedido.atualizado_em = datetime.now()

        # Atualizar relacionamento com Produto
        produto_id = form_data['produtos']
        produto = produtoMp_model.Produto.query.get(produto_id)
        pedido.produto = produto

        # Atualizar relacionamento com Cliente
        cliente_id = form_data['clientes']
        cliente = cliente_model.Cliente.query.get(cliente_id)
        pedido.clientes = [cliente]

        # Atualizar relacionamento com Fornecedor
        fornecedor_id = form_data['fornecedores']
        fornecedor = fornecedor_model.Fornecedor.query.get(fornecedor_id)
        pedido.fornecedores = [fornecedor]

        db.session.commit()
        return pedido
    except Exception as e:
        raise ValueError(str(e))


def remove_pedido(pedido):
    #TODO a função remove_pedido recebe um argumento pedido que representa o pedido a ser removido. A função remove o pedido do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(pedido)
    db.session.commit()


#TODO service para PEDIDO DE PRODUCAO**
def cadastrar_pedidoprod(form_data):
    try:
        form_data['data_entrega'] = datetime.strptime(form_data['data_entrega'], '%Y-%m-%d').date()
        # Certifique se o ID correspondem a instâncias existentes
        filial = filial_pdv_service.listar_filial_pdv_id(form_data['filiais'])

        pedidoprod_bd = pedido_model.PedidoProducao(
            qtde_pedido=form_data.get('qtde_pedido'),
            data_pedido=func.now(),
            data_entrega=form_data.get('data_entrega'),
            status=form_data.get('status'),
            obs=form_data.get('obs'),
            cadastrado_em=func.now(),
            filiais=[filial],  # Adicionando o produto à lista de produtos
            situacao=form_data.get('situacao'),
        )
        if form_data.get('mixprodutos'):
            mixproduto_id = form_data.get('mixprodutos')
            mixproduto_instancia = MixProduto.query.get(mixproduto_id)
            pedidoprod_bd.mixprodutos = mixproduto_instancia

        db.session.add(pedidoprod_bd)
        db.session.commit()
        return pedidoprod_bd
    except Exception as e:
        raise ValueError(str(e))


def listar_pedidosprod():
    #TODO a função listar_pedidos recupera todos os registros da tabela pedido no banco de dados usando pedido_model.pedido.query.all(). Em seguida, retorna uma lista com todos os pedidos encontrados.
    pedidosprod = pedido_model.PedidoProducao.query.all()
    return pedidosprod

def listar_pedidoprod_id(id):
    #TODO a função listar_pedido_id recebe um argumento id e recupera o registro da tabela pedido que corresponde ao id fornecido usando pedido_model.pedido.query.filter_by(id=id).first(). Retorna o pedido encontrado ou None se nenhum pedido correspondente for encontrado.
    pedidoprod = pedido_model.PedidoProducao.query.filter_by(id=id).first()
    return pedidoprod

def atualiza_pedidoproducao(pedido_id, pedido_novo):
    try:
        #TODO a função atualiza_pedido recebe dois argumentos, pedido_anterior e pedido_novo, que representam respectivamente o pedido existente a ser atualizado e os novos dados do pedido. Os atributos do pedido_anterior são atualizados com os valores do pedido_novo. Em seguida, as alterações são commitadas no banco de dados usando db.session.commit().
        pedido_anterior = pedido_model.PedidoProducao.query.get(pedido_id)
        if not pedido_anterior:
            raise ValueError(f"Pedido {pedido_id}não encontrado.")

        pedido_anterior.data_entrega = pedido_novo.get('data_entrega')
        pedido_anterior.qtde_pedido = int(pedido_novo.get('qtde_pedido'))
        pedido_anterior.situacao = int(pedido_novo.get('situacao'))
        pedido_anterior.status = int(pedido_novo.get('status'))
        pedido_anterior.obs = pedido_novo.get('obs')

        # Carregar a instância de MixProduto usando o ID fornecido em pedido_novo
        mixproduto_id = pedido_novo.get('mixprodutos')
        mixproduto = MixProduto.query.get(mixproduto_id)

        # Atribuir a instância de MixProduto ao pedido
        pedido_anterior.mixprodutos = mixproduto

        # Carregar a instância de Filial usando o ID fornecido em pedido_novo
        filial_id = pedido_novo['filiais']
        filial = Filial.query.get(filial_id)

        # Atribuir a instância de Filial ao pedido
        pedido_anterior.filiais = [filial]
        pedido_anterior.atualizado_em = datetime.utcnow()

        db.session.commit()
        return pedido_anterior
    except Exception as e:
        raise ValueError(str(e))

def remove_pedidoprod(pedidoprod):
    #TODO a função remove_pedido recebe um argumento pedido que representa o pedido a ser removido. A função remove o pedido do banco de dados usando db.session.delete() e faz o commit das alterações usando db.session.commit().
    db.session.delete(pedidoprod)
    db.session.commit()

