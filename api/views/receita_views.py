from api import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, BooleanField, SubmitField, SelectField, FloatField, FieldList, FormField, TextAreaField, IntegerField
from flask_wtf.csrf import CSRFProtect
from wtforms_components import SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, length
from ..models.mix_produto_model import MixProduto
from ..schemas import receita_schema
from flask import request, make_response, jsonify, render_template, redirect, url_for, flash
from ..services import receita_service, cliente_service
from ..models.receita_model import Receita
from ..models.produtoMp_model import Produto
from ..models.cliente_model import Cliente
from ..views.mix_produto_views import MixProdutosForm
from marshmallow.exceptions import ValidationError
from ..paginate import paginate

csrf = CSRFProtect(app)
csrf.init_app(app)

class ReceitaForm(FlaskForm):
    descricao_mix = StringField("Descricao_mix", validators=[DataRequired()])
    modo_preparo = TextAreaField("Modo_preparo", validators=[DataRequired()])
    departamento = StringField('Departamento', validators=[DataRequired()])
    rend_kg = FloatField('Rend_kg', validators=[DataRequired()])
    rend_unid = FloatField('Rend_unid', validators=[DataRequired()])
    validade = SelectField('Dias/Validade', choices=[("10", '10 dias'), ("20", '20 dias'), ("30", '30 dias')], validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    cliente = SelectField('Cliente/Fábrica Relacionada', validators=[DataRequired()], coerce=int)
   # mixproduto = SelectField('Mix Produto', validators=[DataRequired()], coerce=int)
    #quantidade = FloatField('Quantidade', validators=[DataRequired()], default=0)

    submit = SubmitField('Cadastrar Receita')

    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        self.cliente.choices = [(cliente.id, cliente.nome)
                                for cliente in Cliente.query.all()]

        self.status.choices = self.get_status_choices()
        self.validade.choices = self.get_validade_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    @staticmethod
    def get_validade_choices():
        return [("10", '10 dias'), ("20", '20 dias'), ("30", '30 dias')]

    def to_dict(self):
        return {
            "descricao_mix": self.descricao_mix.data,
            "modo_preparo": self.modo_preparo.data,
            "departamento": self.departamento.data,
            "rend_kg": self.rend_kg.data,
            "rend_unid": self.rend_unid.data,
            "validade": self.validade.data,
            "status": self.status.data,
            'cliente': int(self.cliente.data) if self.cliente.data else None,
        }


@app.route('/receitas/formulario', methods=['GET', 'POST', 'PUT'])
def exibir_formreceita():
    form = ReceitaForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            cliente_id = form_data['cliente']
            cliente = cliente_service.listar_cliente_id(cliente_id)

            if cliente is not None:
                receita_bd = receita_service.cadastrar_receita(form_data)
                flash('Receita cadastrada com sucesso!')
                return redirect(url_for('listar_receitas'))
            else:
                flash('Cliente não cadastrado!')
                return redirect(url_for('exibir_formreceita')), 400
        except ValidationError as e:
            flash('Erro ao cadastrar Receita!')
            return redirect(url_for('exibir_formreceita')), 400

    return render_template('receitas/formreceita.html', form=form)


@app.route('/receitas/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_receita(id):
    receita = receita_service.listar_receita_id(id)
    form = ReceitaForm(obj=receita)

    if request.method == 'POST' and form.validate_on_submit():
        form_data = form.to_dict()
        cliente_id = form_data['cliente']
        receita_bd = receita_service.atualizar_receita(receita, cliente_id, form_data)
        flash('Receita atualizada com sucesso!')
        return redirect(url_for('listar_receitas'))
    return render_template('receitas/formreceita.html', form=form, receita=receita)


@app.route('/receitas/buscar', methods=['GET'])
def buscar_receita():
    nome_receita = request.args.get('nome_receita', '').strip().lower()
    resultados = None

    if nome_receita:
        # Lógica para buscar a receita por nome
        receitas = receita_service.listar_receitas()
        resultados = [receita for receita in receitas if nome_receita in receita.descricao_mix.lower()]

    return render_template("receitas/consultar_receita.html", resultados=resultados, nome_receita=nome_receita)

@app.route('/receitas', methods=['GET', 'POST'])
def listar_receitas():
    if request.method == 'GET':
        receitas = receita_service.listar_receitas()
        receitas_data = receita_schema.ReceitaSchema(many=True).dump([receitas])
        return render_template("receitas/receitas.html", receitas=receitas, receitas_data=receitas_data)
      #  return render_template("receitas/receitas2.html", receita=receitas)

        ##return jsonify(receita_schema.ReceitaSchema(many=True).dump(receitas))

@app.route('/receitas/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def visualizar_receita(id):
    receita = receita_service.listar_receita_id(id)
    if not receita:
        return render_template("receitas/receitas.html", error_message="Receita não encontrada"), 404
    if request.method == 'GET':
        receita_data = receita_schema.ReceitaSchema().dump(receita)
        return render_template("receitas/detalhes.html", receita=receita, receita_data=receita_data)
    elif request.method == 'POST':
        form = ReceitaForm(obj=receita)
        if form.validate_on_submit():
            form_data = form.to_dict()
            cliente_id = form_data['cliente']
            cliente = Cliente.query.get(cliente_id)
            receita.descricao_mix = form_data['descricao_mix']
            receita.modo_preparo = form_data['modo_preparo']
            receita.departamento = form_data['departamento']
            receita.rend_kg = form_data['rend_kg']
            receita.rend_unid = form_data['rend_unid']
            receita.validade = form_data['validade']
            receita.status = form_data['status']
            receita.cliente = cliente
            receita_service.atualizar_receita(receita, cliente_id, form_data)
            flash("receita atualizada com sucesso!")
            return redirect(url_for('listar_receitas'))
        return render_template("receitas/formreceita.html", form=form)
    elif request.method == 'DELETE':
        receita_service.remover_receita(receita)
        return render_template(url_for('listar_receitas'))

class AdicionarProdutosForm(FlaskForm):
    produtos = SelectMultipleField('Produtos', coerce=int)
    quantidades = FloatField('Quantidades', render_kw={"placeholder": "Quantidade para cada produto"})
    submit = SubmitField('Adicionar Produtos')

    def __init__(self, *args, **kwargs):
        super(AdicionarProdutosForm, self).__init__(*args, **kwargs)
        self.produtos.choices = [(produto.id, produto.nome)
                                 for produto in Produto.query.all()]

    def to_dict(self):
        return {
            'produtos': self.produtos.data,
            'quantidades': self.quantidades.data
        }

@app.route('/receitas/<int:id>/adicionar_produto', methods=['GET', 'POST', 'PUT'])
def adicionar_produtos_receita(id):
    receita = Receita.query.get_or_404(id)
    form = AdicionarProdutosForm()
    form.produtos.choices = [(produto.id, produto.nome) for produto in Produto.query.all()]
    #form.quantidades.data = form.quantidades
    if request.method == 'POST' and form.validate_on_submit():
        produtos_selecionados = Produto.query.filter(Produto.id.in_(form.produtos.data)).all()

        # Adicionar produtos à receita
        for produto, quantidade in zip(produtos_selecionados, form.quantidades.data):
            mix_produto = MixProduto(receita=receita, produtos=[produto], quantidades=quantidade)
            db.session.add(mix_produto)
        db.session.commit()

        flash("Produtos adicionados com sucesso!")
        return redirect(url_for('visualizar_receita', id=id))
    return render_template('receitas/adicionar_produtos.html', form=form, receita=receita)

@app.route('/receitas/<int:id>/produtosreceita', methods=['GET'])
def listar_produtos_receita(id):
    receita = receita_service.listar_receita_id(id)
    if not receita:
        return render_template("receitas/receitas.html", error_message="Receita não encontrada"), 404
    return render_template("receitas/produtosreceita.html", receita=receita)


@app.route('/receitas/<int:id>/adicionar_produto', methods=['GET', 'POST'])
def adicionar_produtos_receita22(id):
    receita = receita_service.listar_receita_id(id)
    if not receita:
        return render_template("receitas/receitas.html", error_message="Receita não encontrada"), 404
    # Carregar escolhas de produtos no formulário
    form = AdicionarProdutosForm()
    form.produtos.choices = [(produto.id, produto.nome) for produto in Produto.query.all()]
    form.quantidades.data = form.quantidades
    if form.validate_on_submit():
        produtos_selecionados = Produto.query.filter(Produto.id.in_(form.produtos.data)).all()

        # Adicionar produtos à receita
        for produto in produtos_selecionados:
            mix_produto = MixProduto(receita=receita, produto=produto)
            db.session.add(mix_produto)
        db.session.commit()
        flash("Produtos adicionados com sucesso!")
        return redirect(url_for('exibir_formreceita', id=id))
    return render_template('receitas/adicionar_produtos.html', form=form, receita=receita)

@app.route('/receitas/<int:id>/adicionar_produtos', methods=['GET', 'POST'])
def adicionar_produtos(id):
    form = AdicionarProdutosForm()
    receitas = receita_service.listar_receita_id(id)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            receita = Receita.query.get_or_404(id)
            produto_ids = form.produtos.data
            produtos = Produto.query.filter(Produto.id.in_(produto_ids)).all()
            receita.produtos.extend(produtos)
            db.session.add(receita)
            db.session.commit()
            flash("Produtos adicionados com sucesso!")
            return redirect(url_for('exibir_formreceita', id=id))
        except Exception as e:
            return render_template('error.html', message=str(e), status_code=500)
    return render_template('receitas/adicionar_produtos.html', form=form, receita=receitas,)


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


@app.route('/receitas/<int:id>/deletar', methods=['DELETE'])
def deletar_receita(id):
    receita = receita_service.listar_receita_id(id)
    if receita:
        db.session.delete(receita)
        db.session.commit()
    return redirect(url_for('listar_receitas'))
