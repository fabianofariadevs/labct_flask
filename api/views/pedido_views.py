from flask import request, render_template, redirect, url_for, flash
from ..services import pedido_service
from ..models.produtoMp_model import Produto
from ..models.pedido_model import Pedido, PedidoProducao
from ..models.filial_pdv_model import Filial
from ..models.fornecedor_model import Fornecedor
from ..models.receita_model import Receita
from ..schemas import pedido_schemas
from ..models import pedido_model
from api import db, app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError
from sqlalchemy.orm import joinedload

# TODO ** Classe PedidoCForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria

class PedidoCForm(FlaskForm):
    qtde_pedido = StringField("Qtde_Pedido", validators=[DataRequired()])
    #data_pedido = DateField("Data_Pedido", format='%Y-%m-%d',validators=[DataRequired()])
    data_entrega = DateField('Dt_Entrega_limite', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    obs = StringField('obs', validators=[DataRequired()])
    produto_id = SelectField('Produto', validators=[DataRequired()])
    filial_pdv = SelectField('Filial_PDV', validators=[DataRequired()])
    fornecedor_id = SelectField('Fornecedor', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(PedidoCForm, self).__init__(*args, **kwargs)

        self.filial_pdv.choices = [(filial.id, filial.nome)
                                   for filial in Filial.query.all()]
        self.fornecedor_id.choices = [(fornecedor.id, fornecedor.nome)
                                      for fornecedor in Fornecedor.query.all()]
        self.produto_id.choices = [(produto.id, produto.nome)
                                   for produto in Produto.query.all()]
        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    # TODO metodo personalizado para extrair os dados do formulário em um formato serializável, como um dicionário.
    def to_dict(self):
        return {
            'qtde_pedido': self.qtde_pedido.data,
            'data_entrega': self.data_entrega.data.strftime('%Y-%m-%d'),
            'status': self.status.data,
            'obs': self.obs.data,
            'produto_id': self.produto_id.data,
            'filial_pdv': self.filial_pdv.data,
            'fornecedor_id': self.fornecedor_id.data,
        }

@app.route('/pedidos/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_pedido(id):
    pedido = pedido_service.listar_pedido_id(id)
    if not pedido:
        return render_template("pedidos/pedidos.html", error_message="Pedido não encontrado"), 404

    form = PedidoCForm(obj=pedido)
    if form.validate_on_submit():
        pedido_atualizado = Pedido.query.get(id)
        form.populate_obj(pedido_atualizado)
        pedido_service.atualiza_pedido(pedido, pedido_atualizado)
        return redirect(url_for("listar_pedidos"))

    return render_template("pedidos/formpedido.html", pedido=pedido, form=form), 400


@app.route('/pedidos/<int:id>', methods=['GET', 'POST'])
def visualizar_pedido(id):
    # pedido = pedido_service.listar_pedido_id(id)
    # return render_template('pedidos/detalhes.html', pedido=pedido)
    if request.method == 'GET':
        pedido = pedido_service.listar_pedido_id(id)
        if pedido:
            pedido_data = pedido_schemas.PedidoSchema().dump(pedido)

            # Obter o nome do produto
            produto = pedido.produtos
            pedido_data['produto_id'] = produto.nome if produto else 'Produto não encontrado'

            # Obter o nome do fornecedor
            fornecedor = pedido.fornecedor
            pedido_data['fornecedor_id'] = fornecedor.nome if fornecedor else 'Fornecedor não encontrado'

            # Obter o nome da filial
            filial = pedido.filiais
            pedido_data['filial_pdv'] = filial.nome if filial else 'Filial não encontrada'

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

        return render_template("pedidos/pedidos.html", pedidos=pedidos_data, total_pedidos=total_pedidos,
                               total_pedidos_ativos=total_pedidos_ativos,
                               total_pedidos_inativos=total_pedidos_inativos)


@app.route('/pedidos/formulario', methods=['GET', 'POST'])
def fazer_pedido_compra():
    form = PedidoCForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            pedido = pedido_schemas.PedidoSchema().load(form_data)
            pedido_bd = pedido_service.cadastrar_pedido(pedido)
            pedido_data = pedido_schemas.PedidoSchema().dump(pedido_bd)
            flash("Pedido de Compra cadastrado com sucesso!")
            return redirect(url_for("listar_pedidos"))
        except ValidationError as error:
            flash("Erro ao cadastrar Pedido de Compra")
    return render_template('pedidos/formpedido.html', form=form)


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
    data_entrega = DateField('Data_Entrega', format='%Y-%m-%d', validators=[DataRequired()])
    qtde_pedido = StringField("Qtde_Pedido", validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    obs = StringField('Obs', validators=[DataRequired()])
    receita_id = SelectField('Receita', validators=[DataRequired()])
    filial_pdv = SelectField('Filial_pdv', validators=[DataRequired()])

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(PedidoPForm, self).__init__(*args, **kwargs)
        self.receita_id.choices = [(receita.id, receita.descricao_mix)
                                   for receita in Receita.query.all()]
        self.filial_pdv.choices = [(filial.id, filial.nome)
                                   for filial in Filial.query.all()]
        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    def to_dict(
            self):  # metodo personalizado no seu formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
        return {
            'data_entrega': self.data_entrega.data.strftime('%Y-%m-%d'),
            'qtde_pedido': self.qtde_pedido.data,
            'status': self.status.data,
            'obs': self.obs.data,
            'receita_id': self.receita_id.data,
            'filial_pdv': self.filial_pdv.data,
        }

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


@app.route('/pedidoprod/<int:id>', methods=['GET', 'POST'])
def visualizar_pedidoprod(id):
    #pedido = pedido_service.listar_pedido_id(id)
    # return render_template('pedidos/detalhes.html', pedido=pedido)
    if request.method == 'GET':
        pedidoprod = pedido_service.listar_pedidoprod_id(id)
        #pedido = pedido_service.listar_pedido_id(id)
        if pedidoprod:
            pedidoprod_data = pedido_schemas.PedidoProducaoSchema().dump(pedidoprod)
            # Ajusta o formato da hora
            pedidoprod_data['data_pedido'] = pedidoprod.data_pedido.strftime('%d/%m/%Y')
            pedidoprod_data['data_entrega'] = pedidoprod.data_entrega.strftime('%d/%m/%Y')

            # Obter o nome do receita
            receita = pedidoprod.receitas
            pedidoprod_data['receita_id'] = receita.descricao_mix if receita else 'Receita não encontrada'

            # Obter o nome dos filiais relacionados
            filial = pedidoprod.filiais
            pedidoprod_data['filial_pdv'] = filial.nome if filial else 'Produto não encontrada'

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


@app.route('/pedidoprod', methods=['GET'])
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
            pedido_dict['receita_id'] = receita.descricao_mix if receita else 'Receita não encontrado'

            # Obter o nome do Filial
            filial = pedido.filiais
            pedido_dict['filial_pdv'] = filial.nome if filial else 'Filial não encontrado'

            pedidos_data.append(pedido_dict)

        total_pedidosprod = len(pedidosprod)
        total_pedidosprod_ativos = len(
    [pedidoproducao for pedidoproducao in pedidosprod if pedidoproducao.status == 1])
        total_pedidosprod_inativos = len(
            [pedidoproducao for pedidoproducao in pedidosprod if pedidoproducao.status == 0])

        return render_template("pedidos/pedidosprod.html", pedidosprod=pedidos_data, total_pedidosprod=total_pedidosprod,
                               total_pedidosprod_ativos=total_pedidosprod_ativos,
                               total_pedidosprod_inativos=total_pedidosprod_inativos)


@app.route('/pedidoprod/formulario', methods=['GET', 'POST', 'PUT'])
def fazer_pedido_producao():
    form = PedidoPForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            pedidoprod = pedido_schemas.PedidoProducaoSchema().load(form_data)
            pedido_bd = pedido_service.cadastrar_pedidoprod(pedidoprod)
            pedido_data = pedido_schemas.PedidoProducaoSchema().dump(pedido_bd)
            return redirect(url_for("listar_pedidosprod", form=form, form_data=form_data, pedidoprod=pedido_bd))
        except ValidationError as error:
            return render_template('pedidos/formpedidoprod.html', form=form, error_message=error.messages)
    else:
        return render_template('pedidos/formpedidoprod.html', form=form, error_message=form.errors)


@app.route('/pedidoprod/<int:id>/deletar', methods=['DELETE'])
def deletar_pedidoprod(id):
    pedidoprod = pedido_service.listar_pedidoprod_id(id)
    if pedidoprod:
        db.session.delete(pedidoprod)
        db.session.commit()
    return redirect(url_for('listar_pedidosprod')), 200
