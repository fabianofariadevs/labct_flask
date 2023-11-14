from api import db
import datetime
from sqlalchemy import func
from ..models import receita_model, cliente_model
from ..services import cliente_service

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_receita(form_data):
    receita_bd = receita_model.Receita(
        descricao_mix=form_data.get('descricao_mix'),
        modo_preparo=form_data.get('modo_preparo'),
        departamento=form_data.get('departamento'),
        rend_kg=form_data.get('rend_kg'),
        rend_unid=form_data.get('rend_unid'),
        validade=form_data.get('validade'),
        status=form_data.get('status'),
        cadastrado_em=func.now(),
        atualizado_em=form_data.get('atualizado_em'),
        cliente=cliente_service.listar_cliente_id(form_data.get('cliente'))
    )

    db.session.add(receita_bd)
    db.session.commit()
    return receita_bd


def atualizar_receita(receita, cliente_id, form_data):
    if receita:
        cliente = cliente_service.listar_cliente_id(cliente_id)
        if cliente:
            receita.cliente = cliente
            receita.descricao_mix = form_data.get('descricao_mix')
            receita.modo_preparo = form_data.get('modo_preparo')
            receita.departamento = form_data.get('departamento')
            receita.rend_kg = form_data.get('rend_kg')
            receita.rend_unid = form_data.get('rend_unid')
            receita.validade = form_data.get('validade')
            receita.status = form_data.get('status')
            receita.atualizado_em = func.now()
            db.session.commit()
            return receita
        else:
            raise ValueError(f"Cliente não encontrado")
    else:
        raise ValueError(f"Receita não encontrada")

def remover_receita(id):
    receita = receita_model.Receita.query.filter_by(id=id).first()
    db.session.delete(receita)
    db.session.commit()
    return receita

def listar_receitas():
    receitas = receita_model.Receita.query.all()
    return receitas


def listar_receita_id(id):
    receita = receita_model.Receita.query.filter_by(id=id).first()
    return receita

def atualizar_receita99(receita_anterior, receita_novo, form_data):
    if receita_anterior:
        cliente_id = form_data['cliente']
        cliente = cliente_model.Cliente.query.get(cliente_id)
        receita_novo.cliente = cliente
        receita_anterior.descricao_mix = receita_novo.descricao_mix
        receita_anterior.modo_preparo = receita_novo.modo_preparo
        receita_anterior.departamento = receita_novo.departamento
        receita_anterior.rend_kg = receita_novo.rend_kg
        receita_anterior.rend_unid = receita_novo.rend_unid
        receita_anterior.validade = receita_novo.validade
        receita_anterior.status = receita_novo.status
        if receita_anterior.cadastrado_em is None:
            receita_anterior.cadastrado_em = func.now()

        receita_anterior.atualizado_em = func.now()

        db.session.commit()
        db.session.refresh(receita_anterior)
        return receita_anterior
    else:
        raise ValueError(f"Receita não encontrada")

def remove_receita(receita):
    receita = receita_model.Receita.query.filter_by(id=receita.id).first()
    try:
        db.session.delete(receita)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível remover a receita {receita.descricao_mix}. Erro: {e}")


