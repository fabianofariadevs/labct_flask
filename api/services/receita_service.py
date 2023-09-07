import requests
from sqlalchemy import func
from ..models import receita_model, produtoMp_model, receita_produto
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_receita(receita, produto_id, quantidades):
    try:
        receita_bd = receita_model.Receita(descricao_mix=receita.descricao_mix, modo_preparo=receita.modo_preparo, departamento=receita.departamento, rend_kg=receita.rend_kg,
                                           rend_unid=receita.rend_unid, validade=receita.validade, status=receita.status, cadastrado_em=func.now(),
                                           atualizado_em=receita.atualizado_em)

        produtos = produtoMp_model.Produto.query.filter(produtoMp_model.Produto.id.in_(produto_id)).all()

        # Associe os produtos à receita com as quantidades correspondentes
        for produto, quantidade in zip(produtos, quantidades):
            receita_bd.produtos.append(produto)
            receita_bd.quantidades[produto.id] = quantidade

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


def adicionar_produtos_a_receita(receita_id, produtos_quantidades):
    try:
        receita = receita_model.Receita.query.get(receita_id)

        if not receita:
            raise ValueError(f"Receita com ID {receita_id} não encontrada.")

        for produto_id, quantidade in produtos_quantidades.items():
            produto = produtoMp_model.Produto.query.get(produto_id)

            if not produto:
                raise ValueError(f"Produto com ID {produto_id} não encontrado.")

            # Verifique se o produto já está associado à receita
            if produto not in receita.produtos:
                # Se não estiver associado, adicione o produto à receita
                receita.produtos.append(produto)

            # Registre a quantidade associada ao produto na receita
            receita.produto_quantidades[produto] = quantidade

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível adicionar produtos à receita. Erro: {str(e)}")

def obter_produtos_da_receita(receita_id):
    try:
        receita = receita_model.Receita.query.get(receita_id)

        if not receita:
            raise ValueError(f"Receita com ID {receita_id} não encontrada.")

        produtos_da_receita = {}
        for produto, quantidade in receita.produto_quantidades.items():
            produtos_da_receita[produto] = quantidade

        return produtos_da_receita
    except Exception as e:
        raise ValueError(f"Não foi possível obter os produtos da receita. Erro: {str(e)}")