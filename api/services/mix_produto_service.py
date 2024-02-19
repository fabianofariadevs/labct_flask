from api import db
from sqlalchemy import func
from ..models import mix_produto_model, receita_model, produtoMp_model
from ..services import produtoMp_service, receita_service, filial_pdv_service

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def listar_mixprodutos():
    mixproduto = mix_produto_model.MixProduto.query.all()
    return mixproduto

def listar_mixproduto_id(id):
    mixproduto = mix_produto_model.MixProduto.query.filter_by(id=id).first()
    return mixproduto

def cadastrar_mixproduto(form_data):
    produtos_ids = form_data.get('produtos', [])
    if not isinstance(produtos_ids, list):
        produtos_ids = [produtos_ids]

    produtos = produtoMp_model.Produto.query.filter(produtoMp_model.Produto.id.in_(produtos_ids)).all()
    if len(produtos) != len(produtos_ids):
        raise ValueError("Um ou mais produtos não foram encontrados.")

    mixproduto = mix_produto_model.MixProduto(
        cod_prod_mix=form_data['cod_prod_mix'],
        status=form_data['status'],
        situacao=form_data['situacao'],
        produtos=produtos,
        quantidades=form_data['quantidades'],
        receita=receita_service.listar_receita_id(form_data['receita']),
        cadastrado_em=func.now(),
    )
    db.session.add(mixproduto)
    db.session.commit()
    return mixproduto


def salvar_mixproduto(mixproduto):
    db.session.commit()


def cadastrar_mixproduto22(form_data):
    try:
        produtos_com_quantidades = form_data.get('produtos', [])
        if not isinstance(produtos_com_quantidades, list):
            raise ValueError("A lista de produtos não foi enviada")

        for item in produtos_com_quantidades:
            item['quantidade'] = int(item['quantidade'])

            mix_bd = mix_produto_model.MixProduto(
                cod_prod_mix=form_data.cod_prod_mix,
                status=form_data.status,
                situacao=form_data.situacao,
                produtos=[item['produto'] for item in produtos_com_quantidades],
                quantidade=[item['quantidade'] for item in produtos_com_quantidades],
                receita=form_data.receita,
                filiais=form_data.filiais,
                cadastrado_em=func.now(),
                atualizado_em=form_data.atualizado_em,
            )
            db.session.add(mix_bd)
            db.session.commit()
            return mix_bd
    except Exception as e:
        raise ValueError(f"Erro ao cadastrar mixproduto: {e}")

def deletar_mixproduto(mixproduto):
    db.session.delete(mixproduto)
    db.session.commit()


def atualizar_mixproduto(form_data):
    mixproduto = mix_produto_model.MixProduto.query.filter_by(id=form_data.id).first()
    if not mixproduto:
        raise ValueError(f"O mixproduto com id {form_data.id} não foi encontrado.")

    mixproduto.produtos = form_data.produtos
    mixproduto.quantidades = form_data.quantidades
    mixproduto.receita = form_data.receita

    db.session.commit()
    return mixproduto
