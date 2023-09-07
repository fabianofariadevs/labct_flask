#TODO método CRUD
from api import db
from ..models import estoque_model, produtoMp_model


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


def atualizar_estoque_apos_producao(pedido_producao):
    for item in pedido_producao.receita.produtos:
        produto = produtoMp_model.Produto.query.get(item.id)
        estoque = estoque_model.Estoque.query.filter_by(produto_id=produto.id).first()

        if estoque:
            estoque.quantidade_atual += item.quantidade
            db.session.commit()


def solicitar_reposicao(produto_id):
    produto = produtoMp_model.Produto.query.get(produto_id)

    if produto:
        # Crie um registro de solicitação de reposição no banco de dados
        reposicao = estoque_model.ReposicaoEstoque(produto_id=produto_id)
        db.session.add(reposicao)
        db.session.commit()

def atualizar_estoque_minimo(produto, estoque_minimo):
    produto.estoque_minimo = estoque_minimo
    db.session.commit()


