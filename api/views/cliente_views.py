from flask import request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from api import app
from ..models import cliente_model
from ..services import cliente_service, filial_pdv_service
from ..models.cliente_model import Cliente
from ..schemas import cliente_schema, filial_pdv_schema
from ..schemas.cliente_schema import ClienteSchema
from sqlalchemy.orm import joinedload
from ..paginate import paginate
from ..models.filial_pdv_model import Filial
from..views.filial_pdv_views import FilialForm
from typing import Dict

# TODO: Classe ClienteForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('Email@', validators=[DataRequired()])
    responsavel = StringField('Responsavel', validators=[DataRequired()])
    whatsapp = StringField('Whatsapp', validators=[DataRequired()])
    cnpj = StringField('Cnpj')
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    #status = BooleanField('Status')
    filial_id = SelectField('Selecionar Filial', validators=[DataRequired()])

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.filial_id.choices = [(filial.id, filial.nome)
                                  for filial in Filial.query.all()]
        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    def to_dict(self):  # metodo personalizado no seu formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
        return {
            'nome': self.nome.data,
            'endereco': self.endereco.data,
            'bairro': self.bairro.data,
            'cidade': self.cidade.data,
            'estado': self.estado.data,
            'telefone': self.telefone.data,
            'email': self.email.data,
            'responsavel': self.responsavel.data,
            'whatsapp': self.whatsapp.data,
            'cnpj': self.cnpj.data,
            'status': self.status.data,
            'filial_id': self.filial_id.data,
        }

@app.route('/clientes/formulariofilial', methods=['GET', 'POST'])###2
def novoformfilial():
    form = FilialForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            filial = filial_pdv_schema.FilialSchema().load(form_data)
            filial_bd = filial_pdv_service.cadastrar_filial_pdv(filial)
            filial_data = filial_pdv_schema.FilialSchema().dump(filial_bd)
            flash("Filial cadastrada com sucesso!")
            return redirect(url_for('exibir_formulario'))
        except ValidationError as error:
            flash("Erro ao cadastrar filial: " + str(error.messages))
    return render_template('clientes/formfilialnova.html', form=form)###3


@app.route('/clientes/formulario', methods=['GET', 'POST'])
def exibir_formulario():
    formcli = ClienteForm()
    if request.method == 'POST' and formcli.validate_on_submit():
        try:
            form_data = formcli.to_dict()
            cf = cliente_schema.ClienteSchema().load(form_data)
            cliente_bd = cliente_service.cadastrar_cliente(cf)
            cliente_data = cliente_schema.ClienteSchema().dump(cliente_bd)
            flash("Cliente cadastrada com sucesso!")
            # Redirecionar para a página de listagem de clientes após o cadastro bem-sucedido
            return redirect(url_for("listar_clientes"))
        except ValidationError as error:
            flash("Erro ao cadastrar filial: " + str(error.messages))
    return render_template('clientes/formulario.html', form=formcli)


@app.route('/clientes/<int:id>/imprimir', methods=['GET'])
def imprimir_cliente(id):
    clienteimpressao = cliente_service.listar_cliente_id(id)

    if clienteimpressao:
        cliente_data = cliente_schema.ClienteSchema().dump(clienteimpressao)

        return str(cliente_data)
    else:
        return render_template("clientes/cliente.html", error_message="Cliente não encontrado"), 404


@app.route('/clientes/buscar', methods=['GET'])
def buscar_cliente():
    nome_cliente = request.args.get('nome_cliente', '').strip().lower()
    resultados = None

    if nome_cliente:
        # Lógica para buscar o cliente por nome
        clientes = cliente_service.listar_clientes()
        resultados = [cliente for cliente in clientes if nome_cliente in cliente.nome.lower()]
        resultados = []
        for cliente in clientes:
            if nome_cliente in cliente.nome.lower():
                resultados.append(cliente)

    return render_template("clientes/consultar_cliente.html", resultados=resultados, nome_cliente=nome_cliente)


@app.route('/clientes/<int:id>', methods=['GET', 'POST'])
def visualizar_cliente(id): ## OK 0808
    #cliente = cliente_service.listar_cliente_id(id)
    #return render_template('clientes/detalhes.html', cliente=cliente)
    if request.method == 'GET':
        clientev = cliente_service.listar_cliente_id(id)
        if clientev:
            cliente_data = cliente_schema.ClienteSchema().dump(clientev)

            # Obter o nome da filial
            filial = clientev.filial
            cliente_data['filial_id'] = filial.nome if filial else 'Filial não encontrada'

            return render_template('clientes/detalhes.html', clientev=cliente_data)
        else:
            # Caso o pedido não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Cliente não encontrado', status_code=404)

    elif request.method == 'POST':  # Lidar com o método DELETE
        if request.form.get('_method') == 'DELETE':
            clientev = cliente_service.listar_cliente_id(id)
            if clientev:
                cliente_service.deletar_cliente(clientev)
                return redirect(url_for('listar_clientes'))

@app.route('/clientes', methods=['GET'])
def listar_clientes():  #OK 0808
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Escolha o número de clientes por página

    clientes = Cliente.query.options(joinedload('filial')).all()

    clientes_data = []
    for cliente in clientes:
        cliente_dict = cliente_schema.ClienteSchema().dump(cliente)

        # Obter o nome da filial
        filial = cliente.filial
        cliente_dict['filial_id'] = filial.nome if filial else 'Filial não encontrada'

        clientes_data.append(cliente_dict)

    total_clientes = len(clientes)
    total_clientes_ativos = len([cliente for cliente in clientes if cliente.status == 1])
    total_clientes_inativos = len([cliente for cliente in clientes if cliente.status == 0])

    paginated_result = paginate(Cliente.query, ClienteSchema(), page, per_page)

    return render_template("clientes/cliente.html", paginated_result=paginated_result, clientes=clientes_data,
                           total_clientes=total_clientes,
                           total_clientes_ativos=total_clientes_ativos,
                           total_clientes_inativos=total_clientes_inativos)


@app.route('/clientes/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_cliente(id): #OK
    atuacliente = cliente_service.listar_cliente_id(id)
    if not atuacliente:
        #return "Cliente não encontrado", 404
        return render_template("clientes/cliente.html", error_message="Cliente não encontrado"), 404
    form = ClienteForm(obj=atuacliente)
    if form.validate_on_submit():
        cliente_atualizado = cliente_model.Cliente.query.get(id)
        form.populate_obj(cliente_atualizado)
        cliente_service.atualiza_cliente(atuacliente, cliente_atualizado)
        return redirect(url_for("listar_clientes"))

    return render_template("clientes/formulario.html", cliente=atuacliente, form=form), 400

#@app.route('/clientes/<int:id>', methods=['DELETE'])



