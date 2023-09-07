from sqlalchemy import func
from ..models import receita_model, produtoMp_model, receita_produto
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_receita(receita):
    receita_bd = receita_model.Receita(descricao_mix=receita.descricao_mix, modo_preparo=receita.modo_preparo, departamento=receita.departamento, rend_kg=receita.rend_kg,
                                       rend_unid=receita.rend_unid, validade=receita.validade, status=receita.status, cadastrado_em=func.now(),
                                       atualizado_em=receita.atualizado_em, produto_id=receita.produto_id)
    db.session.add(receita_bd)
    db.session.commit()
    return receita_bd

def listar_receitas():
    receitas = receita_model.Receita.query.all()
    return receitas

def listar_receita_id(id):
    receita = receita_model.Receita.query.filter_by(id=id).first()
    return receita

def atualiza_receita(receita_anterior, receita_novo):
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

def remove_receita(receita):
    db.session.delete(receita)
    db.session.commit()

def adicionar_produto_a_receita(receita, produto_id, quantidade):
    produto = produtoMp_model.Produto.query.get(produto_id)
    if not produto:
        raise ValueError(f"Produto com ID {produto_id} não encontrado.")

    # Adiciona o produto à tabela intermediária entre Receitas e Produtos.
    relacao_produto_receitas = db.Table('receitaproduto',
                                        db.Column('receita', db.Integer, db.ForeignKey('receitas.id'),
                                                  primary_key=True),
                                        db.Column('produto_id', db.Integer, db.ForeignKey('produtos.id'),
                                                  primary_key=True), db.Column('quantidade', db.Integer))

    relacao_produto_receitas.insert().values(receita=receita, produto_id=produto.id, quantidade=quantidade)

    db.session.commit()

    # Criar uma associação entre a Receita e o Produto com a quantidade
    #receita.produtos.append(produto)
    #receita.quantidades.append(quantidade)
    #db.session.commit()