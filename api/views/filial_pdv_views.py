from api import app, api, db
from marshmallow.exceptions import ValidationError
from flask import request, render_template, redirect, url_for, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from ..models.filial_pdv_model import Filial
from ..services import filial_pdv_service, cliente_service
from ..schemas import filial_pdv_schema
from ..models.cliente_model import Cliente

#TODO ** Classe FilialForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria

class FilialForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    responsavel = StringField('Responsável', validators=[DataRequired()])
    whatsapp = StringField('WhatsApp', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    cliente = SelectField('Cliente', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(FilialForm, self).__init__(*args, **kwargs)
        self.cliente.choices = [(cliente.id, cliente.nome) for cliente in Cliente.query.all()]
        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

 #TODO metodo personalizado no formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
    def to_dict(self):
        data = {
            'nome': str(self.nome.data) if self.nome.data else '',
            'endereco': str(self.endereco.data) if self.endereco.data else '',
            'bairro': str(self.bairro.data) if self.bairro.data else '',
            'cidade': str(self.cidade.data) if self.cidade.data else '',
            'estado': str(self.estado.data) if self.estado.data else '',
            'responsavel': str(self.responsavel.data) if self.responsavel.data else '',
            'whatsapp': str(self.whatsapp.data) if self.whatsapp.data else '',
            'cnpj': str(self.cnpj.data) if self.cnpj.data else '',
            'status': str(self.status.data) if self.status.data else '',
            'cliente': int(self.cliente.data) if self.cliente.data else None,
        }
        return data


@app.route('/filiais/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_filial(id):
    filial = filial_pdv_service.listar_filial_pdv_id(id)
    form = FilialForm(request.form, obj=filial)
    if request.method == 'POST' and form.validate_on_submit():
        form_data = form.to_dict()
        cliente_id = form_data['cliente']
        cliente = Cliente.query.get(cliente_id)
        filial_atualizada = Filial(nome=form_data['nome'], endereco=form_data['endereco'], bairro=form_data['bairro'],
                                   cidade=form_data['cidade'], estado=form_data['estado'], responsavel=form_data['responsavel'],
                                   whatsapp=form_data['whatsapp'], cnpj=form_data['cnpj'], status=form_data['status'],
                                   cliente=cliente)

        filial_pdv_service.atualiza_filial_pdv(filial, filial_atualizada, form_data)
        flash("Filial atualizada com sucesso!")
        return redirect(url_for('listar_filiais'))

    return render_template('filiais/formfilial.html', form=form, filial=filial), 400


@app.route('/filiais', methods=['GET'])###1
def listar_filiais():
    if request.method == 'GET':
        filiais = filial_pdv_service.listar_filial_pdv()

        return render_template('filiais/filial.html', filiais=filiais)


@app.route('/filiais/formulario', methods=['GET', 'POST'])###2
def exibir_formfilial():
    form = FilialForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            cf = form_data['cliente']
            # Verifique se o cliente existe no banco de dados
            cliente = cliente_service.listar_cliente_id(cf)
            if cliente is None:
                filial_bd = filial_pdv_service.cadastrar_filial_pdv(form_data)
                flash("Filial cadastrada com sucesso!")
                return redirect(url_for('listar_filiais'))
            else:
                flash("Cliente não encontrado!")
                return redirect(url_for('exibir_formfilial')), 400
        except ValidationError as e:
            flash(e.messages)
            return redirect(url_for('exibir_formfilial')), 400
    return render_template('filiais/formfilial.html', form=form)


@app.route('/filiais/buscar', methods=['GET'])
def buscar_filial():
    nome_filial = request.args.get('nome_filial', '').strip().lower()
    resultados = None

    if nome_filial:
        # Lógica para buscar a filial por nome
        filiais = filial_pdv_service.listar_filial_pdv_id(id)
        resultados = [filial for filial in filiais if nome_filial in filial.nome.lower()]

    return render_template("filiais/consultar_filial.html", resultados=resultados, nome_filial=nome_filial)


@app.route('/filiais/<int:id>', methods=['GET', 'POST'])
def visualizar_filial(id):
    filial = filial_pdv_service.listar_filial_pdv_id(id)
    if not filial:
        return render_template("filiais/filial.html", error_message="Filial não encontrada"), 404
    if request.method == 'GET':
        # Carrega os relacionamentos de filial automaticamente com os modelos SQLAlchemy
        filial_data = filial_pdv_schema.FilialSchema().dump(filial)
        return render_template('filiais/detalhes.html', filial=filial_data)
    elif request.method == 'POST':
        form = FilialForm(obj=filial)
        if form.validate_on_submit():
            form_data = form.to_dict()
            cliente_id = form_data['cliente']
            cliente = Cliente.query.get(cliente_id)
            filial.nome = form_data['nome']
            filial.endereco = form_data['endereco']
            filial.bairro = form_data['bairro']
            filial.cidade = form_data['cidade']
            filial.estado = form_data['estado']
            filial.responsavel = form_data['responsavel']
            filial.whatsapp = form_data['whatsapp']
            filial.cnpj = form_data['cnpj']
            filial.status = form_data['status']
            filial.cliente = cliente
            filial_pdv_service.atualiza_filial_pdv(filial, filial)
            flash("Filial atualizada com sucesso!")
            return redirect(url_for('listar_filiais'))
        return render_template('filiais/formfilial.html', form=form)
    elif request.method == 'DELETE':
        filial_pdv_service.remove_filial_pdv(filial)
        return redirect(url_for('listar_filiais'))

@app.route('/filiais/<int:id>', methods=['DELETE'])
def deletar_filial(id):
    filial = filial_pdv_service.listar_filial_pdv_id(id)
    filial_pdv_service.remove_filial_pdv(filial)
    return redirect(url_for('listar_filiais'))


@app.route('/filiais/<int:id>', methods=['GET', 'POST'])
def visualizar(id):
    if request.method == 'GET':
        filial = filial_pdv_service.listar_filial_pdv_id(id)
        if filial:
            filial_data = filial_pdv_schema.FilialSchema().dump(filial)

            # Obter o nome do CLIENTE
            cliente = filial.cliente
            filial_data['cliente'] = cliente.nome if cliente else None

            # Obter o nome do ESTOQUE
            estoques = filial.estoques
            estoques_ids = [estoque.nome if estoque else 'Estoque não encontrado' for estoque in estoques]
            filial_data['estoques'] = estoques_ids

            # Obter o nome do MIXPRODUTO
            mixprodutos = filial.mixprodutos
            mixprodutos_ids = [mixproduto.nome if mixproduto else 'MixProduto não encontrado' for mixproduto in mixprodutos]
            filial_data['mixprodutos'] = mixprodutos_ids

            # Obter o nome do PEDIDO DE PRODUÇAO
            pedidosprod = filial.pedidosprod
            pedidos_producao_ids = [pedido.receita_id if pedido.receitas else 'Pedido de Produção não encontrado' for pedido in pedidosprod]
            filial_data['pedidosprod'] = pedidos_producao_ids

            # varificar se esta em producao
            producao = filial.producoes
            filial_data['producao'] = producao.status if producao else None

            return render_template('filiais/detalhes.html', filial=filial_data)
        else:
            # Caso o pedido não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Pedido não encontrado', status_code=404)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            filial = filial_pdv_service.listar_filial_pdv_id(id)
            if filial:
                filial_pdv_service.remove_filial_pdv(filial)
                return redirect(url_for('listar_filiais'))

