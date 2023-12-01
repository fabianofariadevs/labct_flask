from api import app
from sqlalchemy.orm import joinedload
from ..models.pedido_model import Pedido, PedidoProducao
from ..schemas import estoque_schema, pedido_schemas
from ..models.produtoMp_model import Produto
from ..models.estoque_model import Estoque, ReposicaoEstoque
from flask import request, render_template, jsonify, flash, redirect, url_for
from ..services import estoque_service

#TODO ** Classe EstoqueForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria

@app.route('/estoque/reposicao', methods=['GET', 'POST'])
def solicitar_reposicao(produto_id):
    produto = Produto.query.get(produto_id)

    if produto:
        # Cria um registro de solicitação de reposição no banco de dados
        reposicao = ReposicaoEstoque(produto_id=produto_id)

        flash(f"Solicitação de reposição para o produto {produto.nome} enviada com sucesso!", "success")
    else:
        flash("Produto não encontrado.", "error")

    return redirect(url_for('listar_produtos_reposicao'))


@app.route('/estoques', methods=['GET'])###1
def listar_pal():
    if request.method == 'GET':
        le = estoque_service.listar_estoque()
        listas = estoque_schema.EstoqueSchema().dump(le, many=True)
        return render_template('estoque/estoque.html', le=le, listas=listas)

def listar_produtos_reposicao():
    produtos_reposicao = Produto.query.filter(Produto.quantidade <= Produto.estoque_minimo).all()
    return render_template("estoque/listar_produtos_reposicao.html", produtos_reposicao=produtos_reposicao)


@app.route('/estoque/historicopedidos', methods=['GET'])
def historicopedidos():
    pedidos_data = []
    pedidos = Pedido.query.options(joinedload('produtos')).options(joinedload('fornecedores')).options(joinedload('clientes')).all()
    for pedido in pedidos:
        pedido_dict = pedido_schemas.PedidoSchema().dump(pedido)

        pedido_dict['data_pedido'] = pedido.data_pedido.strftime('%d/%m/%Y')
        pedido_dict['data_entrega'] = pedido.data_entrega.strftime('%d/%m/%Y')

        # Itera sobre a lista de produtos para obter seus nomes
        produtos_nomes = [produto.nome if produto else 'Produto não encontrado' for produto in pedido.produtos]
        pedido_dict['produtos'] = produtos_nomes

        # Obter o nome do fornecedor
        fornecedores_nomes = [fornecedor.nome if fornecedor else 'Fornecedor não encontrado' for fornecedor in pedido.fornecedores]
        pedido_dict['fornecedores'] = fornecedores_nomes

        # Obter o nome do cliente/fabrica
        clientes_nomes = [cliente.nome if cliente else 'Cliente não encontrado' for cliente in pedido.clientes]
        pedido_dict['clientes'] = clientes_nomes

        pedidos_data.append(pedido_dict)

    pedidosprod = PedidoProducao.query.options(joinedload('mixprodutos')).all()
    return render_template("estoque/historicopedidos.html", pedidos=pedidos_data, pedidosprod=pedidosprod)



