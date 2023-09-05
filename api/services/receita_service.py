import requests
from sqlalchemy import func
from ..models import receita_model, produtoMp_model, receita_produto
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_receita(receita, produto_id):
    try:
        receita_bd = receita_model.Receita(descricao_mix=receita.descricao_mix, modo_preparo=receita.modo_preparo, departamento=receita.departamento, rend_kg=receita.rend_kg,
                                           rend_unid=receita.rend_unid, validade=receita.validade, status=receita.status, cadastrado_em=func.now(),
                                           atualizado_em=receita.atualizado_em, produto_id=receita.produto_id)

        produtos = produtoMp_model.Produto.query.filter(produtoMp_model.Produto.id.in_(produto_id)).all()
        receita_bd.produtos = produtos
        db.session.add(receita_bd)
        db.session.commit()
        return receita_bd
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível cadastrar a receita {receita.descricao_mix}. Erro: {e}")

def listar_receitas():
    receitas = receita_model.Receita.query.all()
    return receitas

def listar_receita_id(id):
    receita = receita_model.Receita.query.filter_by(id=id).first()
    return receita

def atualiza_receita(receita_anterior, receita_novo):
    try:
        receita_anterior.descricao_mix = receita_novo.descricao_mix
        receita_anterior.modo_preparo = receita_novo.modo_preparo
        receita_anterior.departamento = receita_novo.departamento
        receita_anterior.rend_kg = receita_novo.rend_kg
        receita_anterior.rend_unid = receita_novo.rend_unid
        receita_anterior.validade = receita_novo.validade
        receita_anterior.status = receita_novo.status
        receita_anterior.cadastrado_em = receita_novo.cadastrado_em
        receita_anterior.atualizado_em = receita_novo.atualizado_em
        receita_anterior.produto_id = receita_novo.produto_id

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível atualizar a receita {receita_novo.descricao_mix}. Erro: {e}")

def remove_receita(receita):
    try:
        db.session.delete(receita)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível remover a receita {receita.descricao_mix}. Erro: {e}")


def adicionar_produto_a_receita(receita, produto, quantidades):
    # Verifique se o produto já está na receita
    if produto in receita.produtos:
        # Se estiver, atualize a quantidade
        receita.produtos[produto] += quantidades
    else:
        # Caso contrário, adicione o produto à receita com a quantidade especificada
        receita.produtos[produto] = quantidades

    db.session.commit()
