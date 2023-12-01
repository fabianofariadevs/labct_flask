from api import db, app
from marshmallow.exceptions import ValidationError
from flask_wtf import FlaskForm
from flask import request, render_template, redirect, url_for, flash
from api.models.mix_produto_model import MixProduto
from api.services import pedido_service, mix_produto_service, filial_pdv_service
from api.models.pedido_model import Pedido, PedidoProducao
from api.models.filial_pdv_model import Filial
from api.schemas import pedido_schemas
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError
from sqlalchemy.orm import joinedload
from datetime import datetime


# TODO ** Classe PedidoPForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria


# TODO métodos para PEDIDOS(COMPRA) E DE (PEDIDOPRODUCAO)
class PedidoPForm(FlaskForm):
    data_entrega = DateField('Data_Entrega', validators=[DataRequired()])
    qtde_pedido = StringField("Qtde_Pedido", validators=[DataRequired()])
    situacao = SelectField('Situação', choices=[("0", 'em Aberto'), ("1", 'em Produção'), ("2", 'Finalizado'), ("3", 'em Distribuição')], validators=[DataRequired()])
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
        self.situacao.choices = self.get_situacao_choices()

        self.status.choices = self.get_status_choices()

    def to_dict(self):
        data = {
            'data_entrega': self.data_entrega.data.strftime('%Y-%m-%d') if self.data_entrega.data else None,
            'qtde_pedido': int(self.qtde_pedido.data) if self.qtde_pedido.data else None,
            "situacao": int(self.situacao.data) if self.situacao.data else None,
            'status': self.status.data,
            'obs': self.obs.data,
            'filiais': int(self.filiais.data) if self.filiais.data else None,
            'mixprodutos': int(self.mixprodutos.data) if self.mixprodutos.data else None,
        }
        return data

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    @staticmethod
    def get_situacao_choices():
        return [("0", 'em Aberto'), ("1", 'em Produção'), ("2", 'Finalizado'), ("3", 'em Distribuição')]

@app.route('/pedidoproducao/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_pedidoprod(id):
    pedidoprod = pedido_service.listar_pedidoprod_id(id)
    if not pedidoprod:
        return render_template("pedidos/formpedidoprod.html", error_message="Pedido não encontrado"), 404

    form = PedidoPForm(obj=pedidoprod)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            form_data['data_entrega'] = datetime.strptime(form_data['data_entrega'], '%Y-%m-%d').date()
            form_data['qtde_pedido'] = int(form_data['qtde_pedido'])
            form_data['situacao'] = int(form_data['situacao'])

            mix_id = form_data['mixprodutos']
            mix_produto_service.listar_mixproduto_id(mix_id)

            filial_id = form_data['filiais']
            filial_pdv_service.listar_filial_pdv_id(filial_id)

            pedido_service.atualiza_pedidoproducao(id, form_data)
            return redirect(url_for('listar_pedidosprod'))
        except ValidationError as error:
            return render_template('error.html', message=error.messages), 400
    return render_template('pedidos/formpedidoprod.html', form=form)


@app.route('/pedidoprod/buscar', methods=['GET'])
def buscar_pedidoprod():
    nome_pedidoprod = request.args.get('nome_pedidoprod', '').strip().lower()
    resultados = []

    if nome_pedidoprod:
        # Lógica para buscar Pedido de Produção por nome RECEITA
        buscapedidosprod = pedido_service.listar_pedidosprod()

        for pedidoproducao in buscapedidosprod:
            descricao_mix = pedidoproducao.receitas.descricao_mix.lower()
            if nome_pedidoprod in descricao_mix:
                resultados.append(pedidoproducao)

    return render_template("pedidos/consultar_pedidoprod.html", resultados=resultados, nome_pedidoprod=nome_pedidoprod)


@app.route('/pedidoproducao/<int:id>', methods=['GET', 'POST'])
def visualizar_pedidoprod(id):
    pedidoprodu = pedido_service.listar_pedidoprod_id(id)
    pedidoprodu_data = pedido_schemas.PedidoProducaoSchema().dump(pedidoprodu)
    for key, value in pedidoprodu_data.items():
        if isinstance(value, str) and not value.isdigit():
            #pedidoprodu_data[key] = None
            continue
        pedidoprodu_data[key] = value

    pedidoprodu_data['data_pedido'] = pedidoprodu.data_pedido.strftime('%d/%m/%Y')
    pedidoprodu_data['data_entrega'] = pedidoprodu.data_entrega.strftime('%d/%m/%Y')

    # Obter o nome do cliente
    cliente = pedidoprodu.cliente
    cliente_info = []
    if cliente:
        cliente_info.append(cliente)
    pedidoprodu_data['cliente'] = cliente_info

    # Obter o nome do mixproduto
    mixproduto = pedidoprodu.mixprodutos
    mixproduto_info = []
    if mixproduto:
        mixproduto_info.append(mixproduto.receita.descricao_mix)
    pedidoprodu_data['mixprodutos'] = mixproduto_info

    # Obter o nome dos filiais relacionados
    filial = pedidoprodu.filiais
    filial_info = []
    if filial:
        filial_info.append(filial)
    pedidoprodu_data['filiais'] = filial_info

    return render_template('pedidos/pedidoprod_detalhes.html', pedidoprodu=pedidoprodu_data)


@app.route('/pedidosproducao', methods=['GET', 'POST'])
def listar_pedidosprod():
    if request.method == 'GET':
        # Carregar os pedidos e usar a opção joinedload para incluir os objetos relacionados (mixprodutos/receita) na consulta
        pedidosproducao = PedidoProducao.query.options(joinedload('mixprodutos')).options(joinedload('filiais')).all()
        pedidos_data = []
        for pedido in pedidosproducao:
            pedido_dict = pedido_schemas.PedidoSchema().dump(pedido)

            pedido_dict['data_pedido'] = pedido.data_pedido.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano
            pedido_dict['data_entrega'] = pedido.data_entrega.strftime('%d/%m/%Y')  # Formata a data como dia/mês/ano

            # Obter o nome das filiais associadas
            filiais = pedido.filiais
            pedido_dict['filiais'] = ', '.join([filial.nome for filial in filiais]) if filiais else 'Filial não encontrado'

            # Obter o nome do MixProduto
            mixproduto = pedido.mixprodutos
            pedido_dict['mixprodutos'] = mixproduto.receita.descricao_mix if mixproduto else 'MixProduto da Receita não encontrado'

            # Obter o dia da produção
            producao = pedido.producoes
            pedido_dict['producoes'] = producao.data_producao if producao else 'Produção não encontrada'

            pedidos_data.append(pedido_dict)

        total_pedidosprod = len(pedidosproducao)
        total_pedidosprod_ativos = len([pedidoprod for pedidoprod in pedidosproducao if pedidoprod.status == 1])
        total_pedidosprod_inativos = len([pedidoprod for pedidoprod in pedidosproducao if pedidoprod.status == 0])

        return render_template("pedidos/pedidosprod.html", pedidosproducao=pedidos_data,
                               total_pedidosprod=total_pedidosprod,
                               total_pedidosprod_ativos=total_pedidosprod_ativos,
                               total_pedidosprod_inativos=total_pedidosprod_inativos)


@app.route('/pedidoproducao/formulario', methods=['GET', 'POST', 'PUT'])
def fazer_pedido_producao():
    form = PedidoPForm()
    form.mixprodutos.choices = [(mixproduto.id, mixproduto.receita.descricao_mix)
                                for mixproduto in MixProduto.query.all()]
    form.filiais.choices = [(filial.id, filial.nome)
                            for filial in Filial.query.all()]
    form.situacao.choices = form.get_situacao_choices()

    form.status.choices = form.get_status_choices()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            # Verificar se os IDs de mixproduto e filial são válidos antes de prosseguir
            mix_id = form_data['mixprodutos']
            if mix_id is not None:
                mixproduto = mix_produto_service.listar_mixproduto_id(mix_id)
                if not mixproduto:
                    flash("MixProduto não encontrado!")
                    return render_template('pedidos/formpedidoprod.html', form=form)
            else:
                flash("MixProduto não encontrado!")
                return render_template('pedidos/formpedidoprod.html', form=form)

            filial_id = form_data['filiais']
            if filial_id is not None:
                filial = filial_pdv_service.listar_filial_pdv_id(filial_id)
                if not filial:
                    flash("Filial não encontrada!")
                    return render_template('pedidos/formpedidoprod.html', form=form)

            else:
                flash("Filial não encontrada!")
                return render_template('pedidos/formpedidoprod.html', form=form)

            # Criar o pedido de produção se tudo estiver correto
            pedido_service.cadastrar_pedidoprod(form_data)
            flash("Pedido de Produção cadastrado com sucesso!")
            return redirect(url_for('listar_pedidosprod'))
        except ValidationError as error:
            # Se ocorrer um erro, forneça informações detalhadas sobre o erro
            return render_template('error.html', message=error.messages), 400
    return render_template('pedidos/formpedidoprod.html', form=form)


@app.route('/historicopedidoproducao', methods=['GET'])
def historicopedidosprod():
    global pedidosprod, total_pedidos_ativos, total_pedidos, total_pedidos_inativos
    pedidos_data = []
    pedidosprod_data = []
    try:
        if request.method == 'GET':
            # Carregar os pedidos e usar a opção joinedload para incluir os objetos relacionados (produtos) na consulta
            pedidos = Pedido.query.options(joinedload('produtos')).options(joinedload('fornecedores')).options(joinedload('clientes')).all()
            for pedido in pedidos:
                pedido_dict = pedido_schemas.PedidoSchema().dump(pedido)

                pedido_dict['data_pedido'] = pedido.data_pedido.strftime('%d/%m/%Y')
                pedido_dict['data_entrega'] = pedido.data_entrega.strftime('%d/%m/%Y')

                # Verificar se o objeto do produto está presente e obter o nome, caso contrário, usar uma mensagem padrão
                produtos_nomes = [produto.nome if produto else 'Produto não encontrado' for produto in pedido.produtos]
                pedido_dict['produtos'] = produtos_nomes

                # Obter o nome do fornecedor
                fornecedores_nomes = [fornecedor.nome if fornecedor else 'Fornecedor não encontrado' for fornecedor in pedido.fornecedores]
                pedido_dict['fornecedores'] = fornecedores_nomes

                # Obter o nome da Fabrica/Cliente
                clientes_nomes = [cliente.nome if cliente else 'Cliente não encontrado' for cliente in pedido.clientes]
                pedido_dict['clientes'] = clientes_nomes

                pedidos_data.append(pedido_dict)

            total_pedidos = len(pedidos)
            total_pedidos_ativos = len([pedido for pedido in pedidos if pedido.status == 1])
            total_pedidos_inativos = len([pedido for pedido in pedidos if pedido.status == 0])

            pedidosprod = PedidoProducao.query.options(joinedload('mixprodutos')).options(joinedload('filiais')).all()

        total_pedidosprod = len(pedidosprod)
        total_pedidosprod_ativos = len([pedidoproducao for pedidoproducao in pedidosprod if pedidoproducao.status == 1])
        total_pedidosprod_inativos = len([pedidoproducao for pedidoproducao in pedidosprod if pedidoproducao.status == 0])

        return render_template("pedidos/historicopedidosprod.html",
                               pedidos=pedidos_data, total_pedidos=total_pedidos,
                               total_pedidos_ativos=total_pedidos_ativos,
                               total_pedidos_inativos=total_pedidos_inativos,

                               pedidosprod=pedidosprod, total_pedidosprod=total_pedidosprod,
                               total_pedidosprod_ativos=total_pedidosprod_ativos,
                               total_pedidosprod_inativos=total_pedidosprod_inativos)
    except ValidationError as error:
        return render_template('error.html', message=error.messages), 400


@app.route('/pedidoprod/<int:id>/deletar', methods=['DELETE'])
def deletar_pedidoprod(id):
    pedidoprod = pedido_service.listar_pedidoprod_id(id)
    if pedidoprod:
        db.session.delete(pedidoprod)
        db.session.commit()
    return redirect(url_for('listar_pedidosprod')), 200
