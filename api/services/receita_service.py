import datetime
from sqlalchemy import func
from ..models import receita_model, produtoMp_model, receita_produto
from api import db

#TODO ** CRUD ** ESSAS funções fornecem operações básicas de criação, leitura, atualização e remoção (CRUD) para os registros da tabela pedido no banco de dados.
#       @author Fabiano Faria

def cadastrar_receita(form_data, produtos_ids, produto_quantidades):
    try:
        produtos = produtoMp_model.Produto.query.filter(produtoMp_model.Produto.id.in_(produtos_ids)).all()
        if not produtos:
            raise ValueError("Nenhum produto válido fornecido para a receita.")

        # Criar uma instância de Receita com base nos dados do formulário
        receita_bd = receita_model.Receita(
            descricao_mix=form_data['descricao_mix'],
            modo_preparo=form_data['modo_preparo'],
            departamento=form_data['departamento'],
            rend_kg=form_data['rend_kg'],
            rend_unid=form_data['rend_unid'],
            validade=form_data['validade'],
            status=form_data['status'],
            cadastrado_em=func.now(),
            atualizado_em=datetime.now(),  # Ajuste conforme necessário
        )

        # Associe os produtos à receita com as quantidades correspondentes
        for produto_id, quantidade in zip(produtos_ids, produto_quantidades):
            produto = produtoMp_model.Produto.query.get(produto_id)
            if not produto:
                raise ValueError(f"Produto com ID {produtos} não encontrado.")

            receita_bd.produtos.append(produto)

            # Crie uma instância de 'receita_produto' com as quantidades fornecidas
            produto_quantidade = produtoMp_model.receita_produto(
                receita_id=receita_bd.id,
                produto_id=produto.id,
                quantidade=quantidade
            )
            db.session.add(produto_quantidade)

        db.session.add(receita_bd)
        db.session.commit()

        return receita_bd

    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível cadastrar a receita. Erro: {e}")


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
        receita_anterior.ingredientes = receita_novo.ingredientes
        receita_anterior.filiais = receita_novo.filiais
        receita_anterior.clientes = receita_novo.clientes
       # receita_anterior.pedidosprod = receita_novo.pedidosprod

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


def obter_produtos_da_receita(receita_id):
    try:
        receita = receita_model.Receita.query.get(receita_id)

        if not receita:
            raise ValueError(f"Receita com ID {receita_id} não encontrada.")

        # Acesse os produtos relacionados à receita (você deve ter um relacionamento definido em seu modelo)
        produtos_da_receita = receita.produtos

        # Aqui, você pode retornar os produtos como uma lista, dicionário ou da maneira que preferir
        # Por exemplo, para retornar um dicionário de produtos e quantidades:
        produtos_quantidades = {produto.nome: quantidade for
                                produto, quantidade in produtos_da_receita}

        return produtos_quantidades

    except Exception as e:
        raise ValueError(f"Não foi possível obter os produtos da receita. Erro: {str(e)}")


def adicionar_produtos_e_quantidades_a_receita(receita_id, produtos_quantidades):
    try:
        # Verifique se produtos_quantidades é um dicionário
        if not isinstance(produtos_quantidades, dict):
            raise ValueError("produtos_quantidades deve ser um dicionário válido.")

        receita = receita_model.Receita.query.get(receita_id)

        if not receita:
            raise ValueError(f"Receita com ID {receita_id} não encontrada.")

        for produto_nome, quantidade in produtos_quantidades.items():
            # Verifique se o produto existe no banco de dados ou adicione-o, se necessário
            produto = produtoMp_model.receita_produto.query.filter_by(nome=produto_nome).first()
            if not produto:
                produto = produtoMp_model.Produto(nome=produto_nome)
                db.session.add(produto)

            # Verifique se o produto já está na receita
            produto_na_receita = next((p for p in receita.produtos if p.nome == produto.nome), None)

            if produto_na_receita:
                # Atualize a quantidade do produto na receita
                produto_na_receita.quantidade += quantidade
            else:
                # Adicione o produto à receita
                receita.produtos.append(produtoMp_model.receita_produto(produto_id=produto.id, quantidade=quantidade))

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível adicionar produtos à receita. Erro: {str(e)}")


def zzadicionar_produtos_e_quantidades_a_receita(receita_id, produtos_quantidades):
    try:
        # Verifique se produtos_quantidades é um dicionário
        if not isinstance(produtos_quantidades, dict):
            raise ValueError("produtos_quantidades deve ser um dicionário válido.")

        receitaprod = receita_model.Receita.query.get(receita_id)

        if not receitaprod:
            raise ValueError(f"Receita com ID {receita_id} não encontrada.")

        for produtos, quantidades in produtos_quantidades.items():
            if produtos in receitaprod.produtos_quantidades:
             # Atualize a quantidade do produto na receita
                receita_produtos = next(filter(lambda p: p.produtos == produtos, receitaprod.produtos_quantidades))
                receita_produtos.quantidade += quantidades
            else:
                # Adicione o produto à receita
                receita_produtos = produtoMp_model.receita_produto(
                    receita_id=receita_id,
                    produto_id=produtos,
                    quantidade=quantidades
                )
                receitaprod.produtos_quantidades.append(receita_produtos)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Não foi possível adicionar produtos à receita. Erro: {str(e)}")
