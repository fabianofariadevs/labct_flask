from sqlalchemy.orm import joinedload

from ..models.pedido_model import Pedido, PedidoProducao
from ..schemas import estoque_schema, pedido_schemas
from flask import request, render_template, jsonify
from ..entidades import estoque
from ..schemas.pedido_schemas import PedidoProducaoSchema, PedidoSchema
from ..services import estoque_service
from api import app
from flask_jwt_extended import jwt_required
from ..services.pedido_service import listar_pedidos, listar_pedidosprod

#TODO ** Classe EstoqueForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria

@app.route('/estoques', methods=['GET'])###1
def listar_pal():
    if request.method == 'GET':
        le = estoque_service.listar_estoque()
        listas = estoque_schema.EstoqueSchema().dump(le, many=True)
        return render_template('estoque/estoque.html', le=le, listas=listas)


@app.route('/historicopedidos', methods=['GET'])
def historicopedidos():
    global pedidosprod, total_pedidos_ativos, total_pedidos, total_pedidos_inativos
    pedidos_data = []
    pedidosprod_data = []

    if request.method == 'GET':
        # Carregar os pedidos e usar a opção joinedload para incluir os objetos relacionados (produtos) na consulta
        pedidos = Pedido.query.options(joinedload('produtos')).all()
        for pedido in pedidos:
            pedido_dict = pedido_schemas.PedidoSchema().dump(pedido)

            pedido_dict['data_pedido'] = pedido.data_pedido.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano
            pedido_dict['data_entrega'] = pedido.data_entrega.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano

            # Verificar se o objeto do produto está presente e obter o nome, caso contrário, usar uma mensagem padrão
            produto = pedido.produtos
            pedido_dict['produto_id'] = produto.nome if produto else 'Produto não encontrado'

            # Obter o nome do fornecedor
            fornecedor = pedido.fornecedor
            pedido_dict['fornecedor_id'] = fornecedor.nome if fornecedor else 'Fornecedor não encontrado'

            # Obter o nome da filial
            filial = pedido.filiais
            pedido_dict['filial_pdv'] = filial.nome if filial else 'Filial não encontrada'

            pedidos_data.append(pedido_dict)

        total_pedidos = len(pedidos)
        total_pedidos_ativos = len([pedido for pedido in pedidos if pedido.status == 1])
        total_pedidos_inativos = len([pedido for pedido in pedidos if pedido.status == 0])

        pedidosprod = PedidoProducao.query.options(joinedload('receitas')).all()
        for pedido in pedidosprod:
            pedido_dict = pedido_schemas.PedidoProducaoSchema().dump(pedido)

            pedido_dict['data_pedido'] = pedido.data_pedido.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano
            pedido_dict['data_entrega'] = pedido.data_entrega.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano

            # Verificar se o objeto da Receita está presente e obter o nome, caso contrário, usar uma mensagem padrão
            receita = pedido.receitas
            pedido_dict['receita_id'] = receita.descricao_mix if receita else 'Receita não encontrado'

            # Obter o nome do Filial
            filial = pedido.filiais
            pedido_dict['filial_pdv'] = filial.nome if filial else 'Filial não encontrado'

            pedidosprod_data.append(pedido_dict)

    total_pedidosprod = len(pedidosprod)
    total_pedidosprod_ativos = len([pedidoproducao for pedidoproducao in pedidosprod if pedidoproducao.status == 1])
    total_pedidosprod_inativos = len([pedidoproducao for pedidoproducao in pedidosprod if pedidoproducao.status == 0])

    return render_template("estoque/historicopedidos.html",
                           pedidos=pedidos_data, total_pedidos=total_pedidos,
                           total_pedidos_ativos=total_pedidos_ativos,
                           total_pedidos_inativos=total_pedidos_inativos,

                           pedidosprod=pedidosprod_data, total_pedidosprod=total_pedidosprod,
                           total_pedidosprod_ativos=total_pedidosprod_ativos,
                           total_pedidosprod_inativos=total_pedidosprod_inativos)





