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

def remover_mixproduto_id(id):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(id=id).first()
    db.session.delete(mixproduto)
    db.session.commit()
    return mixproduto

def listar_mixproduto_produto_id(id):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(produto_id=id).first()
    return mixproduto

def listar_filial_mixproduto_id(id):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(filial_id=id).first()
    return mixproduto

def listar_mixproduto_cliente_id(id):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(cliente_id=id).first()
    return mixproduto

def listar_mixproduto_usuario_id(id):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(usuario_id=id).first()
    return mixproduto

def listar_mixproduto_status(status):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(status=status).first()
    return mixproduto

def listar_mixproduto_situacao(situacao):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(situacao=situacao).first()
    return mixproduto

def listar_mixproduto_cod_prod_mix(cod_prod_mix):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(cod_prod_mix=cod_prod_mix).first()
    return mixproduto

def listar_mixproduto_departamento(departamento):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(departamento=departamento).first()
    return mixproduto

def listar_mixproduto_rend_kg(rend_kg):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(rend_kg=rend_kg).first()
    return mixproduto

def listar_mixproduto_rend_unid(rend_unid):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(rend_unid=rend_unid).first()
    return mixproduto

def listar_mixproduto_validade(validade):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(validade=validade).first()
    return mixproduto

def listar_mixproduto_cadastrado_em(cadastrado_em):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(cadastrado_em=cadastrado_em).first()
    return mixproduto

def listar_mixproduto_atualizado_em(atualizado_em):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(atualizado_em=atualizado_em).first()
    return mixproduto

def listar_mixproduto_receita_id(id):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(receita_id=id).first()
    return mixproduto

def listar_mixproduto_filial_id(id):
    mixproduto = mix_produto_model.Mixproduto.query.filter_by(filial_id=id).first()
    return mixproduto


def editar_mixproduto(mixproduto, id):
    mixproduto_bd = listar_mixproduto_id(id)
    if mixproduto_bd is None:
        return None
    mixproduto_bd.cliente = mixproduto.cliente
    mixproduto_bd.cod_prod_mix = mixproduto.cod_prod_mix
    mixproduto_bd.produto = mixproduto.produto
    mixproduto_bd.descricao = mixproduto.descricao
    mixproduto_bd.modo_preparo = mixproduto.modo_preparo
    mixproduto_bd.departamento = mixproduto.departamento
    mixproduto_bd.rend_kg = mixproduto.rend_kg
    mixproduto_bd.rend_unid = mixproduto.rend_unid
    mixproduto_bd.validade = mixproduto.validade
    mixproduto_bd.status = mixproduto.status
    mixproduto_bd.cadastrado_em = mixproduto.cadastrado_em
    mixproduto_bd.atualizado_em = mixproduto.atualizado_em
    db.session.commit()
    return mixproduto_bd

def remover_mixproduto(id):
    mixproduto = listar_mixproduto_id(id)
    if mixproduto is None:
        return None
    db.session.delete(mixproduto)
    db.session.commit()
    return mixproduto


def listar_receitas_por_mixproduto(id):
    return None


def listar_receita_por_mixproduto(id, id_receita):
    return None


def adicionar_receita_por_mixproduto(id, id_receita):
    return None


def remover_receita_por_mixproduto(id, id_receita):
    return None


def listar_filiais_por_mixproduto(id):
    return None


def listar_filial_por_mixproduto(id, id_filial):
    return None


def listar_pedidos_por_mixproduto(id):
    return None


def listar_pedido_por_mixproduto(id, id_pedido):
    return None


def adicionar_pedido_por_mixproduto(id, id_pedido):
    return None


def remover_pedido_por_mixproduto(id, id_pedido):
    return None


def listar_pedidosprod_por_mixproduto(id):
    return None


def listar_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def adicionar_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def remover_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_filiais_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_filial_por_pedidoprod_por_mixproduto(id, id_pedido, id_filial):
    return None


def remover_filial_por_pedidoprod_por_mixproduto(id, id_pedido, id_filial):
    return None


def listar_pedidos_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_pedido_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_filiais_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_filial_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido, id_filial):
    return None


def remover_filial_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido, id_filial):
    return None


def listar_pedidos_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def remover_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_filiais_por_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_filial_por_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido, id_filial):
    return None


def remover_filial_por_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido, id_pedido1, id_filial):
    return None


def listar_pedidos_por_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_pedido_por_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_filiais_por_pedido_por_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido):
    return None


def listar_filial_por_pedido_por_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido, id_filial):
    return None


def adicionar_filial_por_pedido_por_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido, id_pedido1,
                                                                                    id_pedido2, id_pedido3, id_filial):
    return None


def remover_filial_por_pedido_por_pedido_por_pedido_por_pedidoprod_por_mixproduto(id, id_pedido, id_filial):
    return None


def adicionar_filial_por_pedidoprod_por_mixproduto(id, id_pedido, id_filial):
    return None


def adicionar_filial_por_mixproduto(id, id_filial):
    return None


def remover_filial_por_mixproduto(id, id_filial):
    return None