from sqlalchemy import func
from ..models import filial_pdv_model, cliente_model
from ..services import cliente_service
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_filial_pdv(form_data):
    # Crie uma instância da Filial usando os dados fornecidos
    filial_bd = filial_pdv_model.Filial(
        nome=form_data.get('nome'),
        endereco=form_data.get('endereco'),
        bairro=form_data.get('bairro'),
        cidade=form_data.get('cidade'),
        estado=form_data.get('estado'),
        responsavel=form_data.get('responsavel'),
        whatsapp=form_data.get('whatsapp'),
        cnpj=form_data.get('cnpj'),
        status=form_data.get('status'),
        cadastrado_em=func.now(),
        atualizado_em=form_data.get('atualizado_em'),
        cliente=cliente_service.listar_cliente_id(form_data.get('cliente'))
    )

    db.session.add(filial_bd)
    db.session.commit()

    return filial_bd


def listar_filial_pdv():
    filiais = filial_pdv_model.Filial.query.all()
    return filiais

def listar_filial_pdv_id(id):
    filial_pdv = filial_pdv_model.Filial.query.filter_by(id=id).first()
    return filial_pdv

def atualiza_filial_pdv(filial_pdv_anterior, filial_pdv_novo, form_data):
    if filial_pdv_anterior:
        # Atualiza o cliente da filial
        cliente_id = form_data['cliente']
        cliente = cliente_model.Cliente.query.get(cliente_id)
        filial_pdv_novo.cliente = cliente
        filial_pdv_anterior.nome = filial_pdv_novo.nome
        filial_pdv_anterior.endereco = filial_pdv_novo.endereco
        filial_pdv_anterior.bairro = filial_pdv_novo.bairro
        filial_pdv_anterior.cidade = filial_pdv_novo.cidade
        filial_pdv_anterior.estado = filial_pdv_novo.estado
        filial_pdv_anterior.responsavel = filial_pdv_novo.responsavel
        filial_pdv_anterior.whatsapp = filial_pdv_novo.whatsapp
        filial_pdv_anterior.cnpj = filial_pdv_novo.cnpj
        filial_pdv_anterior.status = filial_pdv_novo.status
        filial_pdv_anterior.atualizado_em = func.now()

        db.session.commit()
        db.session.refresh(filial_pdv_anterior)
        return filial_pdv_anterior
    else:
        raise ValueError(f"Filial não encontrada")

def remove_filial_pdv(filial):
    filial = filial_pdv_model.Filial.query.filter_by(id=filial.id).first()
    if not filial:
        raise ValueError(f"A filial com id {filial.id} não foi encontrada.")
    else:
        db.session.delete(filial)
        db.session.commit()
        return filial


