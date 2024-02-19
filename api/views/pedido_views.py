from api import db, app
from marshmallow.exceptions import ValidationError
from flask_wtf import FlaskForm
from flask_jwt_extended import jwt_required
from flask import request, render_template, redirect, url_for, flash
from api.models.produtoMp_model import Produto
from api.models.pedido_model import Pedido
from api.models.cliente_model import Cliente
from api.models.fornecedor_model import Fornecedor
from api.schemas import pedido_schemas
from api.services import produtoMp_service, fornecedor_service, cliente_service, pedido_service
from wtforms import StringField, SubmitField, SelectField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from sqlalchemy.orm import joinedload
from datetime import datetime


# TODO ** Classe PedidoCForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria

class PedidoCForm(FlaskForm):
    qtde_pedido = StringField("Qtde_Pedido", validators=[DataRequired()])
    data_entrega = DateField('Dt_Entrega_limite', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    obs = StringField('obs', validators=[DataRequired()])
    produtos = SelectField('Produtos', coerce=int)
    clientes = SelectField('Clientes', validators=[DataRequired()], coerce=int)
    fornecedores = SelectField('Fornecedores', validators=[DataRequired()], coerce=int)

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(PedidoCForm, self).__init__(*args, **kwargs)

        self.clientes.choices = [(cliente.id, cliente.nome)
                                 for cliente in Cliente.query.all()]
        self.fornecedores.choices = [(fornecedor.id, fornecedor.nome)
                                     for fornecedor in Fornecedor.query.all()]
        self.produtos.choices = [(produto.id, produto.nome)
                                 for produto in Produto.query.all()]
        self.status.choices = self.get_status_choices()

    # TODO metodo personalizado para extrair os dados do formulário em um formato serializável, como um dicionário.
    def to_dict(self):
        data = {
            'qtde_pedido': int(self.qtde_pedido.data) if self.qtde_pedido.data else None,
            'data_entrega': self.data_entrega.data.strftime('%Y-%m-%d') if self.data_entrega.data else None,
            'status': self.status.data,
            'obs': self.obs.data,
            'clientes': int(self.clientes.data) if self.clientes.data else None,
            'fornecedores': int(self.fornecedores.data) if self.fornecedores.data else None,
            'produtos': int(self.produtos.data) if self.produtos.data else None,
        }
        return data

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

@app.route('/pedidodecompra/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_pedidocompra(id):
    pedidoc = pedido_service.listar_pedido_id(id)
    if not pedidoc:
        return render_template("pedidos/formpedido.html", error_message="Pedido não encontrado"), 404

    form = PedidoCForm(obj=pedidoc)
    if request.method == 'PUT' and form.validate_on_submit():
        try:
            pedido_service.atualiza_pedidoc(pedidoc, form.to_dict(), form)
            flash(f"Pedido {pedidoc.produtos} atualizado com sucesso!")
            return redirect(url_for("listar_pedidos"))
        except ValidationError as error:
            flash("Erro ao atualizar Pedido: {}".format(error.messages))
            return render_template("pedidos/formpedido.html", pedidoc=pedidoc, form=form), 400

    elif request.method == 'POST' and form.validate_on_submit():
        #obter id produto selecionado
        produto_id = form.produtos.data
        #atualiza o produto associado ao pedido
        produtos = produtoMp_service.listar_produto_id(produto_id)
        qtde = form.qtde_pedido.data
        #obter id cliente selecionado
        cliente_id = form.clientes.data
        #atualiza o cliente associado ao pedido
        clientes = cliente_service.listar_cliente_id(cliente_id)
        #obter id fornecedor selecionado
        fornecedor_id = form.fornecedores.data
        #atualiza o fornecedor associado ao pedido
        fornecedores = fornecedor_service.listar_fornecedor_id(fornecedor_id)

        pedido_service.atualiza_pedidoc(pedidoc, form.to_dict(), form)
        flash("Pedido atualizado com sucesso!")
        return redirect(url_for("listar_pedidos"))

    return render_template("pedidos/formpedido.html", pedidoc=pedidoc, form=form), 400


@app.route('/pedidoscompra/buscar', methods=['GET'])
def buscar_pedido():
    nome_pedido = request.args.get('nome_pedido', '').strip().lower()
    resultados = None

    if nome_pedido:
        # Lógica para buscar Pedido de Compra por nome
        pedidos = pedido_service.listar_pedidos()
        resultados = [pedido for pedido in pedidos if nome_pedido in str(pedido.produtos.nome).lower()]

    return render_template("pedidos/consultar_pedidoc.html", resultados=resultados, nome_pedido=nome_pedido)


@app.route('/pedidoscompra/<int:id>', methods=['GET', 'POST'])
def visualizar_pedido(id):
    pedidoc = pedido_service.listar_pedido_id(id)
    if request.method == 'GET':
        pedidos_data = []
        if pedidoc:
            pedido_data = pedido_schemas.PedidoSchema().dump(pedidoc)
            # Ajusta o formato da hora
            pedido_data['data_pedido'] = pedidoc.data_pedido.strftime('%d/%m/%Y')
            pedido_data['data_entrega'] = pedidoc.data_entrega.strftime('%d/%m/%Y')

            # Itera sobre a lista de produtos para obter seus nomes
            produtos_nomes = [produto.nome if produto else 'Produto não encontrado' for produto in pedidoc.produtos]
            pedido_data['produtos'] = produtos_nomes

            # Obter o nome do fornecedor
            fornecedores_nomes = [fornecedor.nome if fornecedor else 'Fornecedor não encontrado' for fornecedor in pedidoc.fornecedores]
            pedido_data['fornecedores'] = fornecedores_nomes

            # Obter o nome do cliente/fabrica
            clientes_nomes = [cliente.nome if cliente else 'Cliente não encontrado' for cliente in pedidoc.clientes]
            pedido_data['clientes'] = clientes_nomes

            pedidos_data.append(pedido_data)

            pedido_service.listar_pedido_id(id)

            return render_template('pedidos/detalhes.html', pedidoc=pedido_data)
        else:
            # Caso o pedido não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Pedido não encontrado', status_code=404)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            pedido = pedido_service.listar_pedido_id(id)
            if pedido:
                pedido_service.remove_pedido(pedido)
                return redirect(url_for('listar_pedidos'))


@app.route('/pedidosdecompras', methods=['GET'])
def listar_pedidos():
    #pedidos = pedido_service.listar_pedidos()
    if request.method == 'GET':
        # Carregar os pedidos e usar a opção joinedload para incluir os objetos relacionados (produtos) na consulta
        pedidos = Pedido.query.options(joinedload('produtos')).options(joinedload('fornecedores')).options(joinedload('clientes')).all()
        pedidos_data = []

        for pedido in pedidos:
            pedido_dict = pedido_schemas.PedidoSchema().dump(pedido)

            pedido_dict['data_pedido'] = pedido.data_pedido.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano
            pedido_dict['data_entrega'] = pedido.data_entrega.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano

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

        total_pedidos = len(pedidos)
        total_pedidos_ativos = len([pedido for pedido in pedidos if pedido.status == 1])
        total_pedidos_inativos = len([pedido for pedido in pedidos if pedido.status == 0])

        return render_template("pedidos/pedidos.html", pedidos=pedidos_data, total_pedidos=total_pedidos,
                               total_pedidos_ativos=total_pedidos_ativos,
                               total_pedidos_inativos=total_pedidos_inativos)


@app.route('/pedidoscompra/formulario', methods=['GET', 'POST', 'PUT'])
def fazer_pedido_compra():
    formpc = PedidoCForm()
    formpc.produtos.choices = [(produto.id, produto.nome)
                               for produto in Produto.query.all()]
    formpc.clientes.choices = [(cliente.id, cliente.nome)
                               for cliente in Cliente.query.all()]
    formpc.fornecedores.choices = [(fornecedor.id, fornecedor.nome)
                                   for fornecedor in Fornecedor.query.all()]
    if request.method == 'POST' and formpc.validate_on_submit():
        try:
            form_data = formpc.to_dict()
            pedido_bd = pedido_service.cadastrar_pedidoc(form_data)
            pedido_schemas.PedidoSchema().dump(pedido_bd)
            flash("Pedido de Compra cadastrado com sucesso!")
            return redirect(url_for("listar_pedidos"))
        except ValidationError as error:
            return render_template("pedidos/formpedido.html", error_message="Erro ao cadastrar Pedido de Compra: {}".format(error.messages)), 400
    return render_template('pedidos/formpedido.html', form=formpc)


@app.route('/pedidoscompra/formulario', methods=['GET', 'POST'])
def fazer_pedido_compra2511():
    formpc = PedidoCForm()
    if request.method == 'POST' and formpc.validate_on_submit():
        form_data = formpc.to_dict()
        produto_id = form_data['produtos']
        produto = produtoMp_service.listar_produto_id(produto_id)
        if produto is None:
            flash("Produto não encontrado!")
            return render_template('pedidos/formpedido.html', form=formpc)

        fornecedor_id = form_data['fornecedores']
        fornecedor = fornecedor_service.listar_fornecedor_id(fornecedor_id)
        if fornecedor is None:
            flash("Fornecedor não encontrado!")
            return render_template('pedidos/formpedido.html', form=formpc)

        cliente_id = form_data['clientes']
        cliente = cliente_service.listar_cliente_id(cliente_id)
        if cliente is None:
            flash("Cliente não encontrado!")
            return render_template('pedidos/formpedido.html', form=formpc)
        try:
            pedido_bd = pedido_service.cadastrar_pedidoc(form_data)
            pedido_schemas.PedidoSchema().dump(pedido_bd)
            flash("Pedido de Compra cadastrado com sucesso!")
            return redirect(url_for("listar_pedidos"))
        except ValidationError as error:
            flash("Erro ao cadastrar Pedido de Compra: {}".format(error.messages))
    else:
        flash("Erro ao cadastrar Pedido de Compra!")
    return render_template('pedidos/formpedido.html', form=formpc)


@app.route('/pedidos/<int:id>/deletar', methods=['DELETE'])
def deletar_pedido(id):
    pedido = pedido_service.listar_pedido_id(id)
    if pedido:
        db.session.delete(pedido)
        db.session.commit()
    return redirect(url_for('listar_pedidos')), 200
