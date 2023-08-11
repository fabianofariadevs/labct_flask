#TODO método CRUD
from api import db
from ..models import estoque_model


#TODO * Definição do CRUD_Modelo para Estoque, ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#     @author Fabiano Faria
def listar_estoque():
    estoques = estoque_model.Estoque.query.all()
    return estoques

def listar_estoque_id(id):
    estoque = estoque_model.Estoque.query.filter_by(id=id).first()
    return estoque

def cadastrar_estoque(estoque):
    estoque_bd = estoque_model.Estoque(nome=estoque.nome, validade=estoque.validade, valor_ultima_compra=estoque.valor_ultima_compra, quantidade_op=estoque.quantidade_op,
                                       quantidade_minima=estoque.quantidade_minima, obs=estoque.obs, produto_id=estoque.produto_id, cliente_id=estoque.cliente_id)
    db.session.add(estoque_bd)
    db.session.commit()
    return estoque_bd

def atualizar_estoque(estoque, estoque_novo):
    estoque.nome = estoque_novo.nome
    estoque.validade = estoque_novo.validade
    estoque.valor_ultima_compra = estoque_novo.valor_ultima_compra
    estoque.quantidade_op = estoque_novo.quantidade_op
    estoque.quantidade_minima = estoque_novo.quantidade_minima
    estoque.obs = estoque_novo.obs
    estoque.produto_id = estoque_novo.produto_id
    estoque.cliente_id = estoque_novo.cliente_id

    db.session.commit()
    return estoque

def excluir_estoque(estoque):
    db.session.delete(estoque)
    db.session.commit()

def altera_saldo_estoque(estoque_id, operacao, tipo_funcao, valor_antigo=None):
    # tipo_funcao -> 1 = Cadastro de Operação // PEDIDO COMPRAS
    # tipo_funcao -> 2 = Atualização de Operação // PEDIDO PRODUÇÃO
    # tipo_função -> 3 = Remoção de Operação
    estoque = listar_estoque_id(estoque_id)
    if tipo_funcao == 1:
        if operacao.tipo == "compra":
            estoque.quantidade_op += operacao.custo
        else:
            estoque.valor -= operacao.custo
    elif tipo_funcao == 2:
        if operacao.tipo == "compra":
            estoque.quantidade_op -= valor_antigo
            estoque.quantidade_op += operacao.custo
        else:
            estoque.quantidade_op += valor_antigo
            estoque.quantidade_op -= operacao.custo
    else:
        if operacao.tipo.value == "compra":
            estoque.quantidade_op -= operacao.custo
        else:
            estoque.quantidade_op += operacao.custo

    db.session.commit()


