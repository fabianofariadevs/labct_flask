from api import db
from ..models import operacao_model
from ..services import estoque_service

def listar_operacoes():
    operacoes = operacao_model.Operacao.query.all()
    return operacoes

def listar_operacao_id(id):
    operacao = operacao_model.Operacao.query.filter_by(id=id).first()
    return operacao

def cadastrar_operacao(operacao):
    operacao_bd = operacao_model.Operacao(
        cliente_id=operacao.cliente_id, #nome
        produto_id=operacao.produto_id, #resumo
        qtde=operacao.qtde, #custo
        tipo=operacao.tipo,
        estoque_id=operacao.estoque_id #conta
    )
    db.session.add(operacao_bd)
    db.session.commit()
    estoque_service.altera_saldo_estoque(operacao.estoque_id, operacao, 1)

    return operacao_bd

def atualizar_operacao(operacao, operacao_nova):
    valor_antigo = operacao.qtde
    operacao.cliente_id = operacao_nova.cliente_id
    operacao.estoque_id = operacao_nova.estoque_id
    operacao.qtde = operacao_nova.qtde
    operacao.tipo = operacao_nova.tipo
    operacao.estoque_id = operacao_nova.estoque_id
    db.session.commit()
    estoque_service.altera_saldo_estoque(operacao_nova.estoque_id, operacao_nova, 2, valor_antigo)
    return operacao

def exclui_operacao(operacao):
    db.session.delete(operacao)
    db.session.commit()
    estoque_service.altera_saldo_estoque(operacao.conta_id, operacao, 3)

