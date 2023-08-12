from flask import render_template, url_for, request, redirect, flash
from sqlalchemy.exc import IntegrityError
from ..models.produtoMp_model import Inventario, Produto
from api import api, app, db
from ..services import fornecedor_service
from ..schemas import produtoMp_schema, fornecedor_schemas
from ..models.fornecedor_model import Fornecedor
from ..models import fornecedor_model
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectField, SelectMultipleField, widgets, \
    DateField
from wtforms.validators import DataRequired, ValidationError
from ..models.estoque_model import Estoque

class FornecedorForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    descricao = StringField("Descrição", validators=[DataRequired()])
    endereco = StringField('Endereco', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('Email@', validators=[DataRequired()])
    responsavel = StringField('Responsavel', validators=[DataRequired()])
    whatsapp = StringField('Whatsapp', validators=[DataRequired()])
    cnpj = StringField('Cnpj', validators=[DataRequired()])
    #status = db.Column(db.Boolean, default=1, nullable=True)
    status = SelectField('Status', choices=[(True, 'Ativo'), (False, 'Inativo')], validators=[DataRequired()])
    #status = BooleanField('Status')
    cadastrado_em = DateField('cadastro dt', format='%d/%m/%Y', validators=[DataRequired()])
    atualizado_em = DateField('atual dt', format='%d/%m/%Y', validators=[DataRequired()])
    produtos = StringField('Produto Ofertado', validators=[DataRequired()])
    # produtos = SelectMultipleField('Produtos', coerce=int, validators=[DataRequired()], widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    #cliente_id = SelectField('Cliente/Fabrica')

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(FornecedorForm, self).__init__(*args, **kwargs)
        self.produtos.choices = [(produto.id, produto.nome) for produto in Produto.query.all()]
      #  self.receitas.choices = [(receita.id, receita.nome) for receita in Receita.query.all()]
        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    def to_dict(self):  # metodo personalizado no seu formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
        return {
            'nome': self.nome.data,
            'descricao': self.descricao.data,
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
            'cadastrado_em': self.cadastrado_em.data,
            'atualizado_em': self.atualizado_em.data,
            'produtos': self.produtos.data,
            #'cliente_id': self.cliente_id.data,
        }


@app.route('/fornecedores', methods=['GET'])
def listar_fornecedores():
    if request.method == 'GET':
        fornecedores = fornecedor_service.listar_fornecedores()
        fornecedores_data = fornecedor_schemas.FornecedorSchema().dump(fornecedores, many=True)
        total_fornecedores = len(fornecedores)
        total_fornecedores_ativos = len([fornecedor for fornecedor in fornecedores if fornecedor.status == 1])
        total_fornecedores_inativos = len([fornecedor for fornecedor in fornecedores if fornecedor.status == 0])

        return render_template("fornecedores/fornecedor.html", fornecedores=fornecedores_data, total_fornecedores=total_fornecedores,
                               total_fornecedores_ativos=total_fornecedores_ativos,
                               total_fornecedores_inativos=total_fornecedores_inativos)


@app.route('/fornecedores/<int:id>', methods=['GET', 'PUT'])
def visualizar_fornecedor(id):
    fornecedor = fornecedor_service.listar_fornecedor_id(id)
    return render_template('fornecedores/detalhes.html', fornecedor=fornecedor)


@app.route('/fornecedores/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_fornecedor(id):
    fornecedor = fornecedor_service.listar_fornecedor_id(id)
    if not fornecedor:
        return render_template("fornecedores/fornecedor.html", error_message="Fornecedor não encontrado"), 404

    form = FornecedorForm(obj=fornecedor)
    if request.method == 'POST' and form.validate_on_submit():
        fornecedor_atualizado = fornecedor_model.Fornecedor.query.get(id)
        # Atualizar os campos do fornecedor
        form.populate_obj(fornecedor_atualizado)
        fornecedor_service.atualiza_fornecedor(fornecedor, fornecedor_atualizado)
        return redirect(url_for("listar_fornecedores"))

    return render_template("fornecedores/formfornecedor.html", fornecedor=fornecedor, form=form), 400


@app.route('/fornecedores/formulario', methods=['GET', 'POST', 'PUT'])
def exibir_formfornecedor():
    form = FornecedorForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            produtos_ids = form_data.pop('produtos', [])  # Remover a lista de IDs de produtos dos dados do formulário
            fornecedor = fornecedor_schemas.FornecedorSchema().load(form_data)

            # Carregar os objetos Produto correspondentes aos IDs
            produtos = Produto.query.filter(Produto.id.in_(produtos_ids)).all()

            fornecedor_data = fornecedor_schemas.FornecedorSchema().dump(fornecedor)
            return redirect(url_for("listar_fornecedores"))
        except ValidationError as error:
            return render_template('fornecedores/formfornecedor.html', form=form, error_message=error.messages)
    else:
        return render_template('fornecedores/formfornecedor.html', form=form, error_message=form.errors)

@app.route('/fornecedores/<int:id>/deletar', methods=['DELETE'])
def deletar_fornecedor(id):
    fornecedor = fornecedor_service.listar_fornecedor_id(id)
    if fornecedor:
        db.session.delete(fornecedor)
        db.session.commit()
    return redirect(url_for('listar_fornecedores'))
