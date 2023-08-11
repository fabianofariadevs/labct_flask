from ..models import mix_produto_model
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_mixproduto(mixproduto):
    mixproduto_bd = mix_produto_model.Mixproduto(cliente=mixproduto.cliente, cod_prod_mix=mixproduto.cod_prod_mix, produto=mixproduto.produto, descricao=mixproduto.descricao,
                                                 modo_preparo=mixproduto.modo_preparo, departamento=mixproduto.departamento, rend_kg=mixproduto.rend_kg, rend_unid=mixproduto.rend_unid,
                                                 validade=mixproduto.validade, status=mixproduto.status, cadastrado_em=mixproduto.cadastrado_em, atualizado_em=mixproduto.atualizado_em)
    db.session.add(mixproduto_bd)
    db.session.commit()
    return mixproduto_bd

def listar_mixprodutos():
    mixprodutos = mix_produto_model.Mixproduto.query.all()
    return mixprodutos

def listar_mixproduto_id(id):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(id=id).first()
    return mixproduto

def atualiza_mixproduto(mixproduto_anterior, mixproduto_novo):
    mixproduto_anterior.cliente = mixproduto_novo.cliente
    mixproduto_anterior.cod_prod_mix = mixproduto_novo.cod_prod_mix
    mixproduto_anterior.produto = mixproduto_novo.produto
    mixproduto_anterior.descricao = mixproduto_novo.descricao
    mixproduto_anterior.modo_preparo = mixproduto_novo.modo_preparo
    mixproduto_anterior.departamento = mixproduto_novo.departamento
    mixproduto_anterior.rend_kg = mixproduto_novo.rend_kg
    mixproduto_anterior.rend_unid = mixproduto_novo.rend_unid
    mixproduto_anterior.validade = mixproduto_novo.validade
    mixproduto_anterior.status = mixproduto_novo.status
    mixproduto_anterior.cadastrado_em = mixproduto_novo.cadastrado_em
    mixproduto_anterior.atualizado_em = mixproduto_novo.atualizado_em
    db.session.commit()

def remove_mixproduto(mixproduto):
    db.session.delete(mixproduto)
    db.session.commit()
