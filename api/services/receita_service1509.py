from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from ..models import receita_model, produtoMp_model, receita_produto
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_receita(receita, produto_ids, quantidades):
    try:
        produtos = produtoMp_model.Produto.query.filter(produtoMp_model.Produto.id.in_(produto_ids)).all()
        if not produtos:
            raise ValueError("Nenhum produto válido fornecido para a receita.")

        receita_bd = receita_model.Receita(
            descricao_mix=receita.descricao_mix, modo_preparo=receita.modo_preparo, departamento=receita.departamento, rend_kg=receita.rend_kg,
            rend_unid=receita.rend_unid, validade=receita.validade, status=receita.status, cadastrado_em=func.now(), atualizado_em=receita.atualizado_em,
            produto_id=receita.produto_id, quantidade=receita.quantidade, produtos=receita.produtos, filiais=receita.filiais, pedidosprod=receita.pedidosprod)

        # Associe os produtos à receita com as quantidades correspondentes
        for produto_id, quantidade in zip(produto_ids, quantidades):
            produtos_quantidades = produtoMp_model.Produto.query.get(produto_id)
            if not produtos_quantidades:
                raise ValueError(f"Produto com ID {produto_id} não encontrado.")
            receita_bd.produtos.append(produtos_quantidades)
            receita_quantidade = produtoMp_model.receita_produto(
                receita_id=receita_bd.id,
                produto_id=produto_id,
                quantidade=quantidade
            )
            db.session.add(receita_quantidade)

        db.session.add(receita_bd)
        db.session.commit()

        return receita_bd

    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível cadastrar a receita {receita.descricao_mix}. Erro: {e}")

def listar_receitas():
    receitas = receita_model.Receita.query.all()
    return receitas

def listar_produtos():
    return produtoMp_model.Produto.query.all()

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
        receita_anterior.quantidade = receita_novo.quantidade
        receita_anterior.produtos = receita_novo.produtos
        receita_anterior.filiais = receita_novo.filiais
        receita_anterior.pedidosprod = receita_novo.pedidosprod

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
        produtos_da_receita = {}

        if receita:
            produtos_da_receita = {produto_produto.id: quantidade.quantidade for produto_produto, quantidade in receita.produtos_quantidades.items()}

        return produtos_da_receita
    except Exception as e:
        raise ValueError(f"Não foi possível obter os produtos da receita. Erro: {str(e)}")

def adicionar_produtos_e_quantidades_a_receita(receita_id, produto_ids, quantidades):
    try:
        receita = receita_model.Receita.query.get(receita_id)
        produtos_quantidades = {}

        if not receita:
            raise ValueError(f"Receita com ID {receita_id} não encontrada.")

        for produto_id, quantidade in zip(produto_ids, quantidades):
            produto = produtoMp_model.Produto.query.get(produto_id)

            if not produto:
                raise ValueError(f"Produto com ID {produto_id} não encontrado.")

            # Verifique se o produto já está associado à receita
            if produto not in receita.produtos:
                # Se não estiver associado, adicione o produto à receita
                receita.produtos.append(produto)

            # Registre a quantidade associada ao produto na receita
            quantidade_associada = produtoMp_model.receita_produto(
                receita_id=receita_id,
                produto_id=produto_id,
                quantidade=quantidade
            )
            db.session.add(quantidade_associada)
            produtos_quantidades[produto_id] = quantidade

        db.session.commit()
        return produtos_quantidades

    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível adicionar produtos à receita. Erro: {str(e)}")