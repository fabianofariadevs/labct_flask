from ..models import mix_produto_model
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def listar_mixprodutos():
    mixproduto = mix_produto_model.MixProduto.query.all()
    return mixproduto

def listar_mixproduto_id(id):
    mixproduto = mix_produto_model.MixProduto.query.filter_by(id=id).first()
    return mixproduto

def cadastrar_mixproduto(form_data):
    mixproduto_bd = mix_produto_model.MixProduto(produto=form_data.produto, quantidade=form_data.quantidade, receita=form_data.receita)
    db.session.add(mixproduto_bd)
    db.session.commit()
    return mixproduto_bd

def atualizar_mixproduto(form_data):
    mixproduto = mix_produto_model.MixProduto.query.filter_by(id=form_data.id).first()
    if not mixproduto:
        raise ValueError(f"O mixproduto com id {form_data.id} não foi encontrado.")

    mixproduto.produto = form_data.produto
    mixproduto.quantidade = form_data.quantidade
    mixproduto.receita = form_data.receita

    db.session.commit()
    return mixproduto
