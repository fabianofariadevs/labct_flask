from flask import render_template, url_for, request, redirect, flash
from sqlalchemy.orm import joinedload
from marshmallow.exceptions import ValidationError
from api import app, db
from ..services import fornecedor_service
from ..schemas import produtoMp_schema, fornecedor_schemas
from ..models.fornecedor_model import Fornecedor
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, ValidationError

class FornecedorForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    descricao = StringField("Produto a Cadastrar", validators=[DataRequired()])
    endereco = StringField('Endereco', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('Email@', validators=[DataRequired()])
    responsavel = StringField('Responsavel', validators=[DataRequired()])
    whatsapp = StringField('Whatsapp', validators=[DataRequired()])
    cnpj = StringField('Cnpj', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(FornecedorForm, self).__init__(*args, **kwargs)
        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    def to_dict(self):
        data = {
            "nome": self.nome.data,
            "descricao": self.descricao.data,
            "endereco": self.endereco.data,
            "bairro": self.bairro.data,
            "cidade": self.cidade.data,
            "estado": self.estado.data,
            "telefone": self.telefone.data,
            "email": self.email.data,
            "responsavel": self.responsavel.data,
            "whatsapp": self.whatsapp.data,
            "cnpj": self.cnpj.data,
            "status": self.status.data,
        }
        return data


@app.route('/fornecedores', methods=['GET'])
def listar_fornecedores():
    if request.method == 'GET':
        # Carregar os produtos e usar a opção joinedload para incluir os objetos relacionados (produtos) na consulta
        fornecedores = Fornecedor.query.options(joinedload('produtos')).all()
        fornecedores_data = []
        for fornecedor in fornecedores:
            fornecedor_dict = fornecedor_schemas.FornecedorSchema().dump(fornecedor)

           # Verificar se o objeto do Produto está presente e obter o nome, caso contrário, usar uma mensagem padrão
            #produto = fornecedor.produtos
            produtos_nomes = [produto.nome for produto in fornecedor.produtos] if fornecedor.produtos else [
                'Produto não encontrado']
            fornecedor_dict['produtos'] = produtos_nomes

            fornecedores_data.append(fornecedor_dict)

        total_fornecedores = len(fornecedores)
        total_fornecedores_ativos = len([fornecedor for fornecedor in fornecedores if fornecedor.status == 1])
        total_fornecedores_inativos = len([fornecedor for fornecedor in fornecedores if fornecedor.status == 0])

        return render_template("fornecedores/fornecedor.html", fornecedores=fornecedores_data, total_fornecedores=total_fornecedores,
                               total_fornecedores_ativos=total_fornecedores_ativos,
                               total_fornecedores_inativos=total_fornecedores_inativos)


@app.route('/fornecedores/buscar', methods=['GET'])
def buscar_fornecedor():
    nome_fornecedor = request.args.get('nome_fornecedor', '').strip().lower()
    resultados = None

    if nome_fornecedor:
        # Lógica para buscar o fornecedor por nome
        fornecedores = fornecedor_service.listar_fornecedores()
        resultados = [fornecedor for fornecedor in fornecedores if nome_fornecedor in fornecedor.nome.lower()]

    return render_template("fornecedores/consultar_fornecedor.html", resultados=resultados, nome_fornecedor=nome_fornecedor)


@app.route('/fornecedores/<int:id>', methods=['GET', 'POST'])
def visualizar_fornecedor(id):
    #fornecedor = fornecedor_service.listar_fornecedor_id(id)
    #return render_template('fornecedores/detalhes.html', fornecedor=fornecedor)
    if request.method == 'GET':
        fornecedor = fornecedor_service.listar_fornecedor_id(id)
        return render_template('fornecedores/detalhes.html', fornecedor=fornecedor)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            fornecedor = fornecedor_service.listar_fornecedor_id(id)
            if fornecedor:
                fornecedor_service.remove_fornecedor(fornecedor)
                return redirect(url_for('listar_fornecedores'))


@app.route('/fornecedores/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_fornecedor(id):
    fornecedor = fornecedor_service.listar_fornecedor_id(id)
    if not fornecedor:
        return render_template("fornecedores/fornecedor.html", error_message="Fornecedor não encontrado"), 404

    form = FornecedorForm(obj=fornecedor)
    if form.validate_on_submit():
        try:
            fornecedor_atualizado = Fornecedor.query.get(id)
            form.populate_obj(fornecedor_atualizado)
            fornecedor_service.atualiza_fornecedor(fornecedor, fornecedor_atualizado)
            flash("Fornecedor atualizado com sucesso!")
            return redirect(url_for("listar_fornecedores"))
        except ValidationError as error:
            flash("Erro ao atualizar Fornecedor")
    return render_template("fornecedores/formfornecedor.html", fornecedor=fornecedor, form=form, error_message="Fornr Atualizado com Sucesso!"), 400


@app.route('/fornecedores/formulario', methods=['GET', 'POST', 'PUT'])
def exibir_formfornecedor():
    form = FornecedorForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            fornecedor = fornecedor_schemas.FornecedorSchema().load(form_data)
            fornecedor_bd = fornecedor_service.cadastrar_fornecedor(fornecedor)
            fornecedor_data = fornecedor_schemas.FornecedorSchema().dump(fornecedor_bd)
            flash("Fornecedor cadastrado com sucesso!")
            return redirect(url_for("listar_fornecedores"))
        except ValidationError as error:
            flash("Erro ao cadastrar Fornecedor")
    return render_template('fornecedores/formfornecedor.html', form=form)


@app.route('/fornecedores/<int:id>/deletar', methods=['DELETE'])
def deletar_fornecedor(id):
    fornecedor = fornecedor_service.listar_fornecedor_id(id)
    if fornecedor:
        db.session.delete(fornecedor)
        db.session.commit()
    return redirect(url_for('listar_fornecedores'))
