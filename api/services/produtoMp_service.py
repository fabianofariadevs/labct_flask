from sqlalchemy import func

from ..models import produtoMp_model, fornecedor_model
from api import db
from ..services import fornecedor_service

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria


def cadastrar_produto(form_data):
    produto_bd = produtoMp_model.Produto(
        nome=form_data.get('nome'),
        descricao=form_data.get('descricao'),
        quantidade=form_data.get('quantidade'),
        compra_unid=form_data.get('compra_unid'),
        peso_pcte=form_data.get('peso_pcte'),
        valor=form_data.get('valor'),
        custo_ultima_compra=form_data.get('custo_ultima_compra'),
        whatsapp=form_data.get('whatsapp'),
        qrcode=form_data.get('qrcode'),
        status=form_data.get('status'),
        estoque_minimo=form_data.get('estoque_minimo'),
        obs=form_data.get('obs'),
        cadastrado_em=func.now(),
        atualizado_em=form_data.get('atualizado_em'),
        fornecedor=fornecedor_service.listar_fornecedor_id(form_data.get('fornecedor'))
    )

    db.session.add(produto_bd)
    db.session.commit()
    return produto_bd

def listar_produtos():
    produtos = produtoMp_model.Produto.query.all()
    return produtos

def listar_produto_id(id):
    produto = produtoMp_model.Produto.query.filter_by(id=id).first()
    return produto

def atualiza_produto(produto, fornecedor_id, form_data):
    if produto:
        fornecedor = fornecedor_service.listar_fornecedor_id(fornecedor_id)
        if fornecedor:
            campos_obrigatorios = ['nome', 'descricao', 'quantidade', 'compra_unid', 'peso_pcte', 'valor', 'custo_ultima_compra', 'whatsapp', 'qrcode', 'status', 'estoque_minimo', 'obs']
            for campo in campos_obrigatorios:
                if campo not in form_data:
                    raise ValueError(f"Campo obrigatório {campo} não informado")

            produto.fornecedor = fornecedor
            produto.nome = form_data['nome']
            produto.descricao = form_data['descricao']
            produto.quantidade = form_data['quantidade']
            produto.compra_unid = form_data['compra_unid']
            produto.peso_pcte = form_data['peso_pcte']
            produto.valor = form_data['valor']
            produto.custo_ultima_compra = form_data['custo_ultima_compra']
            produto.whatsapp = form_data['whatsapp']
            produto.qrcode = form_data['qrcode']
            produto.status = form_data['status']
            produto.estoque_minimo = form_data['estoque_minimo']
            produto.obs = form_data['obs']
            produto.atualizado_em = func.now()

            db.session.commit()

            return produto
        else:
            raise ValueError(f"Fornecedor não encontrado")
    else:
        raise ValueError(f"Produto não encontrado")

    
def remove_produto(produto):
    db.session.delete(produto)
    db.session.commit()


#TODO Aqui os metodos CRUD da classe INVENTARIO
def cadastrar_inventario(inventario):
    inventario_bd = produtoMp_model.Inventario(nome=inventario.nome, cadastrado_em=inventario.cadastrado_em, atualizado_em=inventario.atualizado_em)

   # for i in produto.fornecedor_id:
    #    fornecedor = listar_produtos(i)
     #   produto_bd.produtos.append(fornecedor)
    db.session.add(inventario_bd)
    db.session.commit()
    return inventario_bd

def listar_inventarios():
    inventarios = produtoMp_model.Inventario.query.all()
    return inventarios

def listar_inventario_id(id):
    inventario = produtoMp_model.Inventario.query.filter_by(id=id).first()
    return inventario

def atualiza_inventario(inventario_anterior, inventario_novo):
    inventario_anterior.nome = inventario_novo.nome
    inventario_anterior.descricao = inventario_novo.descricao

    db.session.commit()

def remove_inventario(inventario):
    db.session.delete(inventario)
    db.session.commit()
