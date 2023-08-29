from flask import request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from reportlab.lib.styles import getSampleStyleSheet
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

@app.route('/clientes/formulariofilial', methods=['GET', 'POST'])
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
            flash("Erro ao cadastrar filial. ")
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
            flash("Erro ao cadastrar Cliente")
    return render_template('clientes/formulario.html', form=formcli)


@app.route('/clientes/<int:id>/imprimir', methods=['GET'])
def imprimir_cliente(id):
    clienteimpressao = cliente_service.listar_cliente_id(id)

    if clienteimpressao:
        cliente_data = cliente_schema.ClienteSchema().dump(clienteimpressao)

        return render_template("clientes/pdf_cliente.html", cliente_data=cliente_data)
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

    return render_template("clientes/consultar_cliente.html", resultados=resultados, nome_cliente=nome_cliente)


@app.route('/clientes/<int:id>', methods=['GET', 'POST'])
def visualizar_cliente(id):
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
            # Caso o cliente não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Cliente não encontrado', status_code=404)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            clientev = cliente_service.listar_cliente_id(id)
            if clientev:
                cliente_service.deletar_cliente(clientev)
                return redirect(url_for('listar_clientes'))

@app.route('/clientes', methods=['GET'])
def listar_clientes():
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
def atualizar_cliente(id):
    atuacliente = cliente_service.listar_cliente_id(id)
    if not atuacliente:
        #return "Cliente não encontrado", 404
        return render_template("clientes/cliente.html", error_message="Cliente não encontrado"), 404

    form = ClienteForm(obj=atuacliente)
    if request.method == 'POST' and form.validate_on_submit():
        cliente_atualizado = cliente_model.Cliente.query.get(id)
        form.populate_obj(cliente_atualizado)
        cliente_service.atualiza_cliente(atuacliente, cliente_atualizado)
        return redirect(url_for("listar_clientes"))

    return render_template("clientes/formulario.html", cliente=atuacliente, form=form), 400


@app.route('/clientes/<int:id>/filiais', methods=['GET', 'POST'])
def listar_filiais_do_cliente(id):
    clientev = cliente_service.listar_cliente_id(id)
    if clientev:
        filiais_do_cliente = clientev.filial  # Obter as filiais do cliente
        #filiais_do_cliente_data = filial_pdv_schema.FilialSchema().dump(filiais_do_cliente, many=True)
     #   total_filiais = len(filiais_do_cliente.all())
        return render_template('clientes/filiais_cliente.html',  cliente=clientev, filiais=filiais_do_cliente)
    else:
        # Caso o cliente não seja encontrado, retorne uma mensagem de erro
        return render_template('error.html', message='Cliente não encontrado', status_code=404)

def listar_filiais():
    if request.method == 'GET':
        filiais = filial_pdv_service.listar_filial_pdv()
        filiais_data = filial_pdv_schema.FilialSchema().dump(filiais, many=True)
        #filiais_data = [filial_pdv_schema.FilialSchema().add_links(filial_data) for filial_data in filiais_data]
        total_filiais = len(filiais)
        total_filiais_ativos = len([filial for filial in filiais if filial.status == 1])
        total_filiais_inativos = len([filial for filial in filiais if filial.status == 0])

        return render_template('filiais/filial.html', filiais=filiais_data, total_filiais=total_filiais,
                               total_filiais_ativos=total_filiais_ativos,
                               total_filiais_inativos=total_filiais_inativos)

# TODO TESTES DE IMPRESSÃO DE PDF
# DAQUI PARA BAIXO É O QUE TENTEI FAZER PARA GERAR O PDF, MAS AINDA NÃO CONSEGUI....

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from flask import send_file

from flask import render_template, make_response
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak

@app.route('/clientes/<int:id>/imprimir', methods=['GET'])
def imprimir_cli(id):
    clienteimpressao = cliente_service.listar_cliente_id(id)

    if clienteimpressao:
        cliente_data = cliente_schema.ClienteSchema().dump(clienteimpressao)
        html = render_template("clientes/pdf_cliente.html", cliente_data=cliente_data)

        pdf = generate_pdf(html)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=cliente.pdf'

        return response
    else:
        return render_template("clientes/cliente.html", error_message="Cliente não encontrado"), 404

def generate_pdf(html):
    doc = SimpleDocTemplate("output.pdf", pagesize=letter)
    styles = getSampleStyleSheet()

    # Remove unsupported HTML attributes from the HTML content
    cleaned_html = remove_unsupported_attributes(html)

    Story = [Paragraph(cleaned_html, style=styles["Normal"])]
    doc.build(Story)

    with open("output.pdf", "rb") as f:
        pdf = f.read()

    return pdf


def remove_unsupported_attributes(html):
    # List of unsupported attributes
    unsupported_attributes = ["rel", "target"]  # Add more if needed

    for attr in unsupported_attributes:
        html = html.replace(f'{attr}=', '')

    return html

@app.route('/clientes/<int:id>/gerar-pdf', methods=['POST'])
def gerar_pdf(id):
    cliente = cliente_service.listar_cliente_id(id)

    if cliente:
        # Renderize o template detalhes_cliente_pdf.html
        html = render_template('clientes/pdf_cliente.html', cliente_data=cliente)

        # Crie um “buffer” para armazenar o PDF em memória
        buffer = BytesIO()

        # Crie o PDF usando a biblioteca reportlab
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []

        styles = getSampleStyleSheet()
        paragraph = Paragraph(html, style=styles["BodyText"])
        story.append(paragraph)

        doc.build(story)

        # Retorne o PDF gerado como um arquivo para ‘download’
        buffer.seek(0)
        return send_file(buffer, attachment_filename='detalhes_cliente.pdf', as_attachment=True)
    else:
        return render_template("clientes/cliente_nao_encontrado.html"), 404

