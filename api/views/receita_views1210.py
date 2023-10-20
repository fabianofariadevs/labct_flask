from api import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField, FloatField, FieldList, FormField, Form, IntegerField, TextAreaField
from wtforms.fields import SelectMultipleField
from wtforms_components import SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, length
from ..schemas import receita_schema
from flask import request, make_response, jsonify, render_template, redirect, url_for, flash, session
from ..services import receita_service
from ..models.receita_model import Receita, Ingredientes
from ..paginate import paginate
from ..models.produtoMp_model import Produto, receita_produto
from ..models.filial_pdv_model import Filial
from ..models.cliente_model import Cliente
from sqlalchemy.orm import joinedload

class IngredienteForm(FlaskForm):
    ingredientes = SelectField('Ingrediente', choices=[], validators=[DataRequired()])
    quantidade = FloatField('Quantidade', validators=[DataRequired()])
    unidade = SelectField('Unidade', choices=[("kg", 'Kg'), ("g", 'Grama'), ("l", 'Litro'), ("ml", 'Mililitro')],
                          validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(IngredienteForm, self).__init__(*args, **kwargs)
        self.ingredientes.choices = [(ingredientes.id, ingredientes.nome)
                                     for ingredientes in Ingredientes.query.all()]

    def to_dict(self):
        return {
            'ingredientes': self.ingredientes.data,
            'quantidade': self.quantidade.data,
            'unidade': self.unidade.data
        }

class ReceitaForm(FlaskForm):
    descricao_mix = StringField("Descricao_mix", validators=[DataRequired()])
    modo_preparo = TextAreaField("Modo_preparo", validators=[DataRequired()])
    departamento = StringField('Departamento', validators=[DataRequired()])
    rend_kg = FloatField('Rend_kg', validators=[DataRequired()])
    rend_unid = FloatField('Rend_unid', validators=[DataRequired()])
    validade = StringField('Validade', default='10 dias')
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    produtos = SelectMultipleField('Produtos', choices=[], validators=[DataRequired()])
    filiais = SelectField('Filial Relacionada')
    clientes = SelectField('Cliente/Fábrica Relacionada')


    submit = SubmitField('Cadastrar Receita')

    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        self.produtos.choices = [(produto.id, produto.nome)
                                 for produto in Produto.query.all()]

        self.filiais.choices = [(filial.id, filial.nome)
                                for filial in Filial.query.all()]

        self.clientes.choices = [(cliente.id, cliente.nome)
                                 for cliente in Cliente.query.all()]

        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    def to_dict(self):  # metodo personalizado no seu formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
        return {
            'descricao_mix': self.descricao_mix.data,
            'modo_preparo': self.modo_preparo.data,
            'departamento': self.departamento.data,
            'rend_kg': self.rend_kg.data,
            'rend_unid': self.rend_unid.data,
            'validade': self.validade.data,
            'status': self.status.data,
            'produtos': self.produtos.data,
            'filiais': self.filiais.data,
            'clientes': self.clientes.data,

        }


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Material {self.nome}>'


class MaterialForm(FlaskForm):
    nome = StringField('Nome do Material', validators=[DataRequired()])
    quantidade = FloatField('Quantidade', validators=[DataRequired()])
    submitmat = SubmitField('Adicionar Material')

class IngredientesForm(FlaskForm):
    ingredientes = SelectField('Ingrediente', choices=[], validators=[DataRequired()])
    quantidade = FloatField('Quantidade', validators=[DataRequired()])
    unidade = SelectField('Unidade', choices=[("kg", 'Kg'), ("g", 'Grama'), ("l", 'Litro'), ("ml", 'Mililitro')],
                          validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(IngredientesForm, self).__init__(*args, **kwargs)
        self.ingredientes.choices = [(ingredientes.id, ingredientes.nome)
                                     for ingredientes in Ingredientes.query.all()]

    def to_dict(self):
        return {
            'ingredientes': self.ingredientes.data,
            'quantidade': self.quantidade.data,
            'unidade': self.unidade.data
        }


@app.route('/cadastro_material', methods=['GET', 'POST'])
def cadastro_material():
    form = MaterialForm()
    if form.validate_on_submit():
        nome = form.nome.data
        quantidade = form.quantidade.data
        material = Material(nome=nome, quantidade=quantidade)
        db.session.add(material)
        db.session.commit()
        return redirect(url_for('cadastro_material'))
    materiais = Material.query.all()
    return render_template('cadastro_material.html', form=form, materiais=materiais)


@app.route('/receitas/formulario', methods=['GET', 'POST'])
def exibir_formreceita():
    form = ReceitaForm()
    form.ingredientes.append_entry()
    produtos_quantidades = session.get('receita_produtos', [])

    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()  # Obter os dados do formulário como um dicionário



            # ... Lógica de validação ...

            produtos_quantidades.append({
                'produtos': form_data['produtos'],
                'quantidades': form_data['quantidades']
            })

            session[
                'receita_produtos'] = produtos_quantidades  # Atualize a sessão com a lista de produtos e quantidades
            session.modified = True

            receita_service.cadastrar_receita(form_data)
            # Redirecionar para a página de listagem de receitas
            flash("Receita cadastrada com sucesso!")

            return redirect(url_for("listar_receitas"))
        except ValidationError as error:
            flash("Erro ao cadastrar Receita: " + str(error.messages))

    # Lidar com adição dinâmica de campos
    if 'adicionar_produto' in request.form:
        form.produtos.choices.append((None, 'Selecione um produto'))
        form.quantidades.choices.append((None, 'Selecione uma quantidade'))
    if 'remover_produto' in request.form:
        index = int(request.form['remover_produto'])
        if index < len(form.produtos.choices):
            form.produtos.choices.pop(index)
            form.quantidades.choices.pop(index)

    return render_template('receitas/formreceita.html', form=form,
                           produtos_cadastrados=produtos_quantidades)


@app.route('/receitas/adicionar_produto_sessao', methods=['GET', 'POST'])
def adicionar_produto_sessao():
    form = ReceitaForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Processar os dados do formulário
            produtos = form.produtos.data
            quantidades = form.quantidades.data

            # Verificar se a quantidade é um número válido
            if not isinstance(quantidades, (int, float)) or quantidades <= 0:
                raise ValueError("Quantidade deve ser um número maior que zero.")

            # Obter o produto
            produto = Produto.query.get(produtos)

            # Verificar se o produto existe
            if not produto:
                raise ValueError("Produto não encontrado.")

            # Obter os produtos da sessão
            receita_produtos = session.get('receita_produtos', [])

            # Adicionar o produto à sessão
            receita_produtos.append({
                'produtos': produtos,
                'quantidades': quantidades
            })

            # Atualizar a sessão
            session['receita_produtos'] = receita_produtos
            session.modified = True

            flash("Produto adicionado com sucesso!")
            return redirect(url_for('exibir_formreceita', produtos=produtos))

        except ValueError as e:
            flash(str(e))

    return render_template('receitas/adicionar_produtos.html', form=form, produtos=Produto.query.all(),
                           receita_produtos=session.get('receita_produtos', []))

@app.route('/receitas/remover_produto', methods=['POST'])
def remover_produto():
    try:
        # Processar os dados do formulário
        receita_id = request.form.get('receita_id')
        produto_id = request.form.get('produto_id')

        # Verificar se a receita e o produto existem
        receita = Receita.query.get(receita_id)
        produto = Produto.query.get(produto_id)

        # Verificar se os campos são válidos
        if not receita or not produto:
            raise ValueError("Receita ou produto não encontrado.")

        # Remover o produto da receita
        receita.produtos.remove(produto)
        db.session.commit()

        flash("Produto removido com sucesso!")
        return redirect(url_for('exibir_formreceita', id=receita_id))
    except Exception as e:
        return render_template('error.html', message=str(e), status_code=500)


# Rota para listar os produtos da receita
@app.route('/receitas/listar_produtos', methods=['GET'])
def listar_produtosreceita():
    # Obter o ID da receita
    receita_id = request.args.get('receita_id')
    form = ReceitaForm()
    produtos_da_receita = session.get('receita_produto', [])
    return render_template('receitas/produto_field.html', form=form, receita_produto=produtos_da_receita)


@app.template_global()
def selecionar_produto_quantidade(produtos_selecionados, quantidades_selecionadas):
    return zip(produtos_selecionados, quantidades_selecionadas)


@app.route('/receitas/buscar', methods=['GET'])
def buscar_receita():
    nome_receita = request.args.get('nome_receita', '').strip().lower()
    resultados = None

    if nome_receita:
        # Lógica para buscar a receita por nome
        receitas = receita_service.listar_receitas()
        resultados = [receita for receita in receitas if nome_receita in receita.descricao_mix.lower()]

    return render_template("receitas/consultar_receita.html", resultados=resultados, nome_receita=nome_receita)


@app.route('/receitas', methods=['GET'])
def listar_receitas():
    if request.method == 'GET':
        receitas = receita_service.listar_receitas()
        receitas_data = receita_schema.ReceitaSchema().dump(receitas, many=True)
        total_receitas = len(receitas)
        total_receitas_ativos = len([receita for receita in receitas if receita.status == 1])
        total_receitas_inativos = len([receita for receita in receitas if receita.status == 0])

        return render_template("receitas/receita.html", receitas=receitas_data, total_receitas=total_receitas,
                               total_receitas_ativos=total_receitas_ativos,
                               total_receitas_inativos=total_receitas_inativos)


@app.route('/receitas/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_receita(id):
    atuareceita = receita_service.listar_receita_id(id)
    if not atuareceita:
        return render_template("receitas/receita.html", error_message="Receita não encontrada"), 404

    form = ReceitaForm(obj=atuareceita)
    if form.validate_on_submit():
        receita_atualizado = Receita.query.get(id)
        form.populate_obj(receita_atualizado)
        receita_service.atualiza_receita(atuareceita, receita_atualizado)
        return redirect(url_for("listar_receitas"))

    return render_template("receitas/formreceita.html", receita=atuareceita, form=form), 400

@app.route('/receitas/<int:id>', methods=['GET', 'POST'])
def visualizar_receita(id):
   # receita = receita_service.listar_receita_id(id)
    #return render_template('receitas/detalhes.html', receita=receita)
    if request.method == 'GET':
        receita = receita_service.listar_receita_id(id)
        if receita:
            receita_data = receita_schema.ReceitaSchema().dump(receita)

            # Obter o Produto
            produto = receita.produtos.first()
            receita_data['produtos'] = produto.nome if produto else 'Produto não encontrada'

            # Obter o nome do filial
            filiais = receita.filiais
            filiais_nomes = [filial.nome if filial else 'filial não encontrado'
                             for filial in filiais]
            receita_data['filiais'] = filiais_nomes

            # Obter o nome do PEDIDO DE PRODUÇAO
            pedidosprod = receita.pedidosprod
            pedidos_producao_ids = [pedidoprod.receita_id if pedidoprod else 'Pedido de Produção não encontrado'
                                    for pedidoprod in pedidosprod]
            receita_data['pedidosprod'] = pedidos_producao_ids

            # Obter o nome do CLIENTE
            clientes = receita.clientes
            clientes_nomes = [cliente.nome if cliente else 'Cliente não encontrado'
                              for cliente in clientes]
            receita_data['clientes'] = clientes_nomes

            produtos_quantidades = receita_service.obter_produtos_da_receita(receita_data['id'])
            receita_data['produtos_quantidades'] = produtos_quantidades

            return render_template('receitas/detalhes.html', receita=receita_data, produtos_quantidades=produtos_quantidades)
        else:
            # Caso o pedido não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Receita não encontrada', status_code=404)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            receita = receita_service.listar_receita_id(id)
            if receita:
                receita_service.remove_receita(receita)
                return redirect(url_for('listar_receitas'))

@app.route('/receitas/<int:id>/deletar', methods=['DELETE'])
def deletar_receita(id):
    receita = receita_service.listar_receita_id(id)
    if receita:
        db.session.delete(receita)
        db.session.commit()
    return redirect(url_for('listar_receitas'))
