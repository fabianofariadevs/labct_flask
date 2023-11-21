from api import db, app
from marshmallow.exceptions import ValidationError
from flask_wtf import FlaskForm
from flask import request, render_template, redirect, url_for, flash
from ..models.mix_produto_model import MixProduto
from ..services import pedido_service, mix_produto_service, filial_pdv_service, fornecedor_service, produtoMp_service, cliente_service
from ..models.produtoMp_model import Produto
from ..models.pedido_model import Pedido, PedidoProducao
from ..models.filial_pdv_model import Filial
from ..models.cliente_model import Cliente
from ..models.fornecedor_model import Fornecedor
from ..schemas import pedido_schemas, mix_produto_schema
from ..models import pedido_model
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError
from sqlalchemy.orm import joinedload

# TODO ** Classe PedidoCForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria

class PedidoCForm(FlaskForm):
    qtde_pedido = StringField("Qtde_Pedido", validators=[DataRequired()])
    #data_pedido = DateField("Data_Pedido", validators=[DataRequired()])
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
            'qtde_pedido': self.qtde_pedido.data,
            #'data_pedido': self.data_pedido.data.strftime('%Y-%m-%d'),
            'data_entrega': self.data_entrega.data.strftime('%Y-%m-%d'),
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


@app.route('/pedidos/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_pedido(id):
    pedido = pedido_service.listar_pedido_id(id)
    if not pedido:
        return render_template("pedidos/formpedido.html", error_message="Pedido não encontrado"), 404

    form = PedidoCForm(obj=pedido)
    if request.method == 'POST' and form.validate_on_submit():
        pedido_atualizado = Pedido.query.get(id)
        form.populate_obj(pedido_atualizado)
        #obter id produto selecionado
        produto_id = form.produtos.data
        #atualiza o produto associado ao pedido
        pedido_atualizado.produtos = Produto.query.get(produto_id)
        #obter id cliente selecionado
        cliente_id = form.clientes.data
        #atualiza o cliente associado ao pedido
        pedido_atualizado.clientes = Cliente.query.get(cliente_id)
        #obter id fornecedor selecionado
        fornecedor_id = form.fornecedores.data
        #atualiza o fornecedor associado ao pedido
        pedido_atualizado.fornecedores = Fornecedor.query.get(fornecedor_id)

        pedido_service.atualiza_pedido(pedido, pedido_atualizado)
        flash("Pedido atualizado com sucesso!")
        return redirect(url_for("listar_pedidos"))

    return render_template("pedidos/formpedido.html", pedido=pedido, form=form), 400

@app.route('/pedidos/buscar', methods=['GET'])
def buscar_pedido():
    nome_pedido = request.args.get('nome_pedido', '').strip().lower()
    resultados = None

    if nome_pedido:
        # Lógica para buscar Pedido de Compra por nome
        pedidos = pedido_service.listar_pedidos()
        resultados = [pedido for pedido in pedidos if nome_pedido in str(pedido.produtos.nome).lower()]

    return render_template("pedidos/consultar_pedidoc.html", resultados=resultados, nome_pedido=nome_pedido)


@app.route('/pedidos/<int:id>', methods=['GET', 'POST'])
def visualizar_pedido191(id):
    if request.method == 'GET':
        pedidos = Pedido.query.options(joinedload('produtos')).all()
        pedidos_data = []
        for pedido in pedidos:
            pedido_dict = pedido_schemas.PedidoSchema().dump(pedido)

            pedido_dict['data_pedido'] = pedido.data_pedido.strftime('%d/%m/%Y')
            pedido_dict['data_entrega'] = pedido.data_entrega.strftime('%d/%m/%Y')

            # Verificar se o objeto do produto está presente e obter o nome, caso contrário, usar uma mensagem padrão
            produto = pedido.produtos
            pedido_dict['produtos'] = produto.nome if produto else 'Produto não encontrado'

            # Obter o nome do fornecedor
            fornecedor = pedido.fornecedores
            pedido_dict['fornecedores'] = fornecedor.nome if fornecedor else 'Fornecedor não encontrado'

            # Obter o nome da Cliente/Fabrica
            cliente = pedido.clientes
            pedido_dict['clientes'] = cliente.nome if cliente else 'Filial não encontrada'

            pedidos_data.append(pedido_dict)

        total_pedidos = len(pedidos)
        total_pedidos_ativos = len([pedido for pedido in pedidos if pedido.status == 1])
        total_pedidos_inativos = len([pedido for pedido in pedidos if pedido.status == 0])

        return render_template("pedidos/pedidos.html", pedidos=pedidos_data, total_pedidos=total_pedidos,
                               total_pedidos_ativos=total_pedidos_ativos,
                               total_pedidos_inativos=total_pedidos_inativos)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            pedido = pedido_service.listar_pedido_id(id)
            if pedido:
                pedido_service.remove_pedido(pedido)
                return redirect(url_for('listar_pedidos'))

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

            # Obter o nome do produto
            produto = pedidoc.produtos
            pedido_data['produtos'] = produto.nome if produto else 'Produto não encontrado'

            # Obter o nome do fornecedor
            fornecedor = pedidoc.fornecedores
            pedido_data['fornecedores'] = fornecedor.nome if fornecedor else 'Fornecedor não encontrado'

            # Obter o nome da Cliente/Fabrica
            cliente = pedidoc.clientes
            pedido_data['clientes'] = cliente.nome if cliente else 'Filial não encontrada'

            pedidos_data.append(pedido_data)

            pedido_service.cadastrar_pedido(pedidoc)

            return render_template('pedidos/detalhes.html', pedido=pedido_data)
        else:
            # Caso o pedido não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Pedido não encontrado', status_code=404)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            pedido = pedido_service.listar_pedido_id(id)
            if pedido:
                pedido_service.remove_pedido(pedido)
                return redirect(url_for('listar_pedidos'))


@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    if request.method == 'GET':
        # Carregar os pedidos e usar a opção joinedload para incluir os objetos relacionados (produtos) na consulta
        pedidos = Pedido.query.options(joinedload('produtos')).all()
        pedidos_data = []
        for pedido in pedidos:
            pedido_dict = pedido_schemas.PedidoSchema().dump(pedido)

            pedido_dict['data_pedido'] = pedido.data_pedido.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano
            pedido_dict['data_entrega'] = pedido.data_entrega.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano

            # Verificar se o objeto do produto está presente e obter o nome, caso contrário, usar uma mensagem padrão
            produto = pedido.produtos
            pedido_dict['produtos'] = produto.nome if produto else 'Produto não encontrado'

            # Obter o nome do fornecedor
            fornecedor = pedido.fornecedores
            pedido_dict['fornecedores'] = fornecedor.nome if fornecedor else 'Fornecedor não encontrado'

            # Obter o nome do cliente/fabrica
            cliente = pedido.clientes
            pedido_dict['clientes'] = cliente.nome if cliente else 'Cliente não encontrada'

            pedidos_data.append(pedido_dict)

        total_pedidos = len(pedidos)
        total_pedidos_ativos = len([pedido for pedido in pedidos if pedido.status == 1])
        total_pedidos_inativos = len([pedido for pedido in pedidos if pedido.status == 0])

        return render_template("pedidos/pedidos.html", pedidos=pedidos_data, total_pedidos=total_pedidos,
                               total_pedidos_ativos=total_pedidos_ativos,
                               total_pedidos_inativos=total_pedidos_inativos)


@app.route('/pedidos/formulario', methods=['GET', 'POST'])
def fazer_pedido_compra():
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
            pedido_bd = pedido_service.cadastrar_pedido(form_data)
            pedido_schemas.PedidoSchema().dump(pedido_bd)
            flash("Pedido de Compra cadastrado com sucesso!")
            return redirect(url_for("listar_pedidos"))
        except ValidationError as error:
            flash("Erro ao cadastrar Pedido de Compra: {}".format(error.messages))
    else:
        flash("Erro ao cadastrar Pedido de Compra!")
    return render_template('pedidos/formpedido.html', form=formpc)


@app.route('/pedidos/formulario', methods=['GET', 'POST'])
def fazer_pedido_compra22():
    formpc = PedidoCForm()
    if not formpc.validate_on_submit():
        flash("Erro ao Cadastrar Pedido de Compra!")
        return render_template('pedidos/formpedido.html', form=formpc)

    if formpc.produtos.data is not None:
        produto = Produto.query.get(formpc.produtos.data)
        if produto is None:
            flash("Produto não encontrado!")
            return render_template('pedidos/formpedido.html', form=formpc)

    if formpc.clientes.data is not None:
        cliente = Cliente.query.get(formpc.clientes.data)
        if cliente is None:
            flash("Cliente não encontrado!")
            return render_template('pedidos/formpedido.html', form=formpc)

    if formpc.fornecedores.data is not None:
        fornecedor = Fornecedor.query.get(formpc.fornecedores.data)
        if fornecedor is None:
            flash("Fornecedor não encontrado!")
            return render_template('pedidos/formpedido.html', form=formpc)

    if formpc.validate_on_submit():
        try:
            form_data = formpc.to_dict()
            pedido = pedido_schemas.PedidoSchema().load(form_data)
            pedido_bd = pedido_service.cadastrar_pedido(pedido)
            pedido_data = pedido_schemas.PedidoSchema().dump(pedido_bd)
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


# TODO ** Classe PedidoPForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria


# TODO métodos para PEDIDOS DE PRODUCAO
class PedidoPForm(FlaskForm):
    #data_pedido = DateField("Data_Pedido", format='%d/%m/%Y',validators=[DataRequired()])
    data_entrega = DateField('Data_Entrega', validators=[DataRequired()])
    qtde_pedido = StringField("Qtde_Pedido", validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    obs = StringField('Obs', validators=[DataRequired()])
    filiais = SelectField('Filial_pdv', validators=[DataRequired()], coerce=int)
    mixprodutos = SelectField('MixProduto', validators=[DataRequired()], coerce=int)

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(PedidoPForm, self).__init__(*args, **kwargs)
        self.filiais.choices = [(filial.id, filial.nome)
                                for filial in Filial.query.all()]
        self.mixprodutos.choices = [(mixproduto.id, mixproduto.receita.descricao_mix or mixproduto.situacao)
                                    for mixproduto in MixProduto.query.all()]
        self.status.choices = self.get_status_choices()

    def to_dict(self):
        data = {
            #'data_pedido': self.data_pedido.data.strftime('%Y-%m-%d'),
            'data_entrega': self.data_entrega.data.strftime('%Y-%m-%d'),
            'qtde_pedido': self.qtde_pedido.data,
            'status': self.status.data,
            'obs': self.obs.data,
            'filiais': int(self.filiais.data) if self.filiais.data else None,
            'mixprodutos': int(self.mixprodutos.data) if self.mixprodutos.data else None,
        }
        return data

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]


@app.route('/pedidoprod/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_pedidoprod(id):
    pedidoprod = pedido_service.listar_pedidoprod_id(id)
    if not pedidoprod:
        return render_template("pedidos/formpedidoprod.html", error_message="Pedido não encontrado"), 404

    form = PedidoPForm(obj=pedidoprod)
    if request.method == 'POST' and form.validate_on_submit():
        pedidoprod_atualizado = pedido_model.PedidoProducao.query.get(id)
        form.populate_obj(pedidoprod_atualizado)
        pedido_service.atualiza_pedidoprod(pedidoprod, pedidoprod_atualizado)
        return redirect(url_for("listar_pedidosprod"))

    return render_template("pedidos/formpedidoprod.html", pedidoprod=pedidoprod, form=form), 400


@app.route('/pedidoprod/buscar', methods=['GET'])
def buscar_pedidoprod():
    nome_pedidoprod = request.args.get('nome_pedidoprod', '').strip().lower()
    resultados = []

    if nome_pedidoprod:
        # Lógica para buscar Pedido de Produção por nome RECEITA
        pedidosprod = pedido_service.listar_pedidosprod()

        for pedidoproducao in pedidosprod:
            descricao_mix = pedidoproducao.receitas.descricao_mix.lower()
            if nome_pedidoprod in descricao_mix:
                resultados.append(pedidoproducao)

    return render_template("pedidos/consultar_pedidoprod.html", resultados=resultados, nome_pedidoprod=nome_pedidoprod)


@app.route('/pedidoproducao/<int:id>', methods=['GET', 'POST'])
def visualizar_pedidoprod(id):
    pedidoprod = pedido_service.listar_pedidoprod_id(id)
    if request.method == 'GET':
        pedidos_data = []
        if pedidoprod:
            pedidoprod_data = pedido_schemas.PedidoProducaoSchema().dump(pedidoprod)
            # Ajusta o formato da hora
            pedidoprod_data['data_pedido'] = pedidoprod.data_pedido.strftime('%d/%m/%Y')
            pedidoprod_data['data_entrega'] = pedidoprod.data_entrega.strftime('%d/%m/%Y')

            # Obter o nome do cliente
            cliente = pedidoprod.cliente
            pedidoprod_data['cliente'] = cliente.nome if cliente else 'Cliente não encontrado'

            # Obter o nome do mixproduto
            mixproduto = pedidoprod.mixprodutos
            pedidoprod_data['mixprodutos'] = mixproduto.situacao if mixproduto else 'MixProduto não encontrado'

            # Obter o nome do receita
            receita = pedidoprod.receitas
            pedidoprod_data['receitas'] = receita.descricao_mix if receita else 'Receita não encontrada'

            # Obter o nome dos filiais relacionados
            filial = pedidoprod.filiais
            pedidoprod_data['filiais'] = filial.nome if filial else 'Produto não encontrada'
            pedidos_data.append(pedidoprod_data)
            pedido_service.cadastrar_pedidoprod(pedidoprod)

            return render_template('pedidos/producaodetalhes.html', pedidoprod=pedidoprod_data)
        else:
            # Caso o pedido não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Pedido de Produção não encontrado', status_code=404)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            pedidoprod = pedido_service.listar_pedidoprod_id(id)
            if pedidoprod:
                pedido_service.remove_pedidoprod(pedidoprod)
                return redirect(url_for('listar_pedidosprod'))


@app.route('/pedidosproducao', methods=['GET'])
def listar_pedidosprod():
    if request.method == 'GET':
        # Carregar os pedidos e usar a opção joinedload para incluir os objetos relacionados (receitas) na consulta
        pedidosprod = PedidoProducao.query.options(joinedload('receitas')).all()
        pedidos_data = []
        for pedido in pedidosprod:
            pedido_dict = pedido_schemas.PedidoSchema().dump(pedido)

            pedido_dict['data_pedido'] = pedido.data_pedido.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano
            pedido_dict['data_entrega'] = pedido.data_entrega.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano

            # Verificar se o objeto da Receita está presente e obter o nome, caso contrário, usar uma mensagem padrão
            receita = pedido.receitas
            pedido_dict['receitas'] = receita.descricao_mix if receita else 'Receita não encontrado'

            # Obter o nome do Filial
            filial = pedido.filiais
            pedido_dict['filiais'] = filial.nome if filial else 'Filial não encontrado'

            # Obter o nome do MixProduto
            mixproduto = pedido.mixprodutos
            pedido_dict['mixprodutos'] = mixproduto.situacao if mixproduto else 'MixProduto não encontrado'

            # Obter o dia da produção
            producao = pedido.producoes
            pedido_dict['producoes'] = producao.dia_producao if producao else 'Produção não encontrada'

            pedidos_data.append(pedido_dict)

        total_pedidosprod = len(pedidosprod)
        total_pedidosprod_ativos = len(
            [pedidoproducao for pedidoproducao in pedidosprod if pedidoproducao.status == 1])
        total_pedidosprod_inativos = len(
            [pedidoproducao for pedidoproducao in pedidosprod if pedidoproducao.status == 0])

        return render_template("pedidos/pedidosprod.html", pedidosprod=pedidos_data, total_pedidosprod=total_pedidosprod,
                               total_pedidosprod_ativos=total_pedidosprod_ativos,
                               total_pedidosprod_inativos=total_pedidosprod_inativos)


@app.route('/pedidoproducao/formulario', methods=['GET', 'POST', 'PUT'])
def fazer_pedido_producao():
    form = PedidoPForm()

    if request.method == 'POST' and form.validate_on_submit():

        form_data = form.to_dict()
        mix_id = form_data['mixprodutos']
        mixproduto = mix_produto_service.listar_mixproduto_id(mix_id)
        if mixproduto is None:
            flash("MixProduto não encontrado!")
            return render_template('pedidos/formpedidoprod.html', form=form)

        filial_id = form_data['filiais']
        filial = filial_pdv_service.listar_filial_pdv_id(filial_id)

        if filial is None:
            flash("Filial não encontrada!")
            return render_template('pedidos/formpedidoprod.html', form=form)

        try:
            pedidoprod_mix = pedido_service.cadastrar_pedidoprod(form_data)
            pedido_schemas.PedidoProducaoSchema().dump(pedidoprod_mix)
            flash("Pedido de Produção Mix Cadastrado com Sucesso!")
            return redirect(url_for("listar_pedidosprod"))
        except ValidationError as error:
            flash("Erro ao cadastrar MixProduto: {}".format(error.messages))
    else:
        flash("Erro ao cadastrar MixProduto!")
    return render_template('pedidos/formpedidoprod.html', form=form)


@app.route('/pedidoprod/formulario', methods=['GET', 'POST', 'PUT'])
def fazer_pedido_producao2():
    form = PedidoPForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            mix_id = form_data['mixprodutos']
            mixproduto = mix_produto_service.listar_mixproduto_id(mix_id)
            if mixproduto is None:
                flash("MixProduto não encontrado!")
                return render_template('pedidos/formpedidoprod.html', form=form)

            filial_id = form_data['filiais']
            filial = filial_pdv_service.listar_filial_pdv_id(filial_id)
            if filial is None:
                flash("Filial não encontrada!")
                return render_template('pedidos/formpedidoprod.html', form=form)

            else:
                pedidoprod_mix = pedido_service.cadastrar_pedidoprod(form_data)
                pedido_schemas.PedidoProducaoSchema().dump(pedidoprod_mix)
                flash("MixProduto cadastrado com sucesso!")
                return redirect(url_for("listar_mixprodutos"))
        except ValidationError as error:
            flash("Erro ao cadastrar MixProduto: {}".format(error.messages))
    else:
        flash("Erro ao cadastrar MixProduto!")
    return render_template('pedidos/formpedidoprod.html', form=form)

@app.route('/historicopedidosprod', methods=['GET'])
def historicopedidosprod():
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
            pedido_dict['produtos'] = produto.nome if produto else 'Produto não encontrado'

            # Obter o nome do fornecedor
            fornecedor = pedido.fornecedores
            pedido_dict['fornecedores'] = fornecedor.nome if fornecedor else 'Fornecedor não encontrado'

            # Obter o nome da Fabrica/Cliente
            cliente = pedido.clientes
            pedido_dict['clientes'] = cliente.nome if cliente else 'Filial não encontrada'

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

    return render_template("pedidos/historicopedidosprod.html",
                           pedidos=pedidos_data, total_pedidos=total_pedidos,
                           total_pedidos_ativos=total_pedidos_ativos,
                           total_pedidos_inativos=total_pedidos_inativos,

                           pedidosprod=pedidosprod_data, total_pedidosprod=total_pedidosprod,
                           total_pedidosprod_ativos=total_pedidosprod_ativos,
                           total_pedidosprod_inativos=total_pedidosprod_inativos)

@app.route('/pedidoprod/<int:id>/deletar', methods=['DELETE'])
def deletar_pedidoprod(id):
    pedidoprod = pedido_service.listar_pedidoprod_id(id)
    if pedidoprod:
        db.session.delete(pedidoprod)
        db.session.commit()
    return redirect(url_for('listar_pedidosprod')), 200
