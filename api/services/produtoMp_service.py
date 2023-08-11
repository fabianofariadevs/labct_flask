from ..models import produtoMp_model, fornecedor_model
from api import db
from ..services import fornecedor_service

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria


def cadastrar_produto(produto):
    produto_bd = produtoMp_model.Produto(nome=produto.nome, descricao=produto.descricao, quantidade=produto.quantidade, fornecedor_id=produto.fornecedor_id,
                                         compra_unid=produto.compra_unid, peso_pcte=produto.peso_pcte, valor=produto.valor, custo_ultima_compra=produto.custo_ultima_compra,
                                         whatsapp=produto.whatsapp, qrcode=produto.qrcode, status=produto.status, cadastrado_em=produto.cadastrado_em, atualizado_em=produto.atualizado_em)

   # for i in produto.fornecedor_id:
    #    fornecedor = listar_produtos(i)
     #   produto_bd.produtos.append(fornecedor)
    db.session.add(produto_bd)
    db.session.commit()
    return produto_bd

def listar_produtos():
    produtos = produtoMp_model.Produto.query.all()
    return produtos

def listar_produto_id(id):
    produto = produtoMp_model.Produto.query.filter_by(id=id).first()
    return produto

def atualiza_produto(produto_anterior, produto_novo):
    produto_anterior.nome = produto_novo.nome
    produto_anterior.descricao = produto_novo.descricao
    produto_anterior.quantidade = produto_novo.quantidade
    produto_anterior.fornecedor_id = produto_novo.fornecedor_id
    #produto_anterior.cliente_id = produto_novo.cliente_id
    produto_anterior.compra_unid = produto_novo.compra_unid
    produto_anterior.peso_pcte = produto_novo.peso_pcte
    produto_anterior.valor = produto_novo.valor
    produto_anterior.custo_ultima_compra = produto_novo.custo_ultima_compra
    produto_anterior.whatsapp = produto_novo.whatsapp
    produto_anterior.qrcode = produto_novo.qrcode
    produto_anterior.status = bool(produto_novo.status)

    db.session.commit()

def remove_produto(produto):
    db.session.delete(produto)
    db.session.commit()



#TODO Aqui os meetodos CRUD da classe INVENTARIO
def cadastrar_inventario(inventario):
    produto_bd = produtoMp_model.Produto(nome=produto.nome, descricao=produto.descricao, quantidade=produto.quantidade, fornecedor_id=produto.fornecedor_id,
                                         compra_unid=produto.compra_unid, peso_pcte=produto.peso_pcte, valor=produto.valor, custo_ultima_compra=produto.custo_ultima_compra,
                                         whatsapp=produto.whatsapp, qrcode=produto.qrcode, status=produto.status, cadastrado_em=produto.cadastrado_em, atualizado_em=produto.atualizado_em)

   # for i in produto.fornecedor_id:
    #    fornecedor = listar_produtos(i)
     #   produto_bd.produtos.append(fornecedor)
    db.session.add(produto_bd)
    db.session.commit()
    return produto_bd

def listar_inventarios():
    inventarios = produtoMp_model.Inventario.query.all()
    return inventarios

def listar_inventario_id(id):
    produto = produtoMp_model.Produto.query.filter_by(id=id).first()
    return produto

def atualiza_inventario(produto_anterior, produto_novo):
    produto_anterior.nome = produto_novo.nome
    produto_anterior.descricao = produto_novo.descricao
    produto_anterior.quantidade = produto_novo.quantidade
    produto_anterior.fornecedor_id = produto_novo.fornecedor_id
    #produto_anterior.cliente_id = produto_novo.cliente_id
    produto_anterior.compra_unid = produto_novo.compra_unid
    produto_anterior.peso_pcte = produto_novo.peso_pcte
    produto_anterior.valor = produto_novo.valor
    produto_anterior.custo_ultima_compra = produto_novo.custo_ultima_compra
    produto_anterior.whatsapp = produto_novo.whatsapp
    produto_anterior.qrcode = produto_novo.qrcode
    produto_anterior.status = bool(produto_novo.status)

    db.session.commit()

def remove_inventario(produto):
    db.session.delete(produto)
    db.session.commit()
