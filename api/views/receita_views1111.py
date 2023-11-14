from api import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField, FloatField, FieldList, FormField, TextAreaField, IntegerField
from flask_wtf.csrf import CSRFProtect
from wtforms_components import SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, length
from ..schemas import receita_schema
from flask import request, make_response, jsonify, render_template, redirect, url_for, flash
from ..services import receita_service, cliente_service
from ..models.receita_model import Receita
from ..paginate import paginate
from ..models.mix_produto_model import MixProduto
from ..models.produtoMp_model import Produto
from ..models.cliente_model import Cliente
from marshmallow.exceptions import ValidationError
from wtforms_alchemy import ModelForm, ModelFormField, model_form_factory

csrf = CSRFProtect(app)
csrf.init_app(app)

BaseModelForm = model_form_factory(FlaskForm)
class MixProdutosForm(BaseModelForm):
    produto = SelectField('Produto', validators=[DataRequired()], coerce=int)
    quantidade = FloatField('Quantidade', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MixProdutosForm, self).__init__(*args, **kwargs)
        self.produto.choices = [(produto.id, produto.nome) for produto in Produto.query.all()]

    def to_dict(self):
        return {
            'produto': self.produto.data,
            'quantidade': self.quantidade.data,
        }

class ReceitaForm(BaseModelForm):
    descricao_mix = StringField("Descricao_mix", validators=[DataRequired()])
    modo_preparo = TextAreaField("Modo_preparo", validators=[DataRequired()])
    departamento = StringField('Departamento', validators=[DataRequired()])
    rend_kg = FloatField('Rend_kg', validators=[DataRequired()])
    rend_unid = FloatField('Rend_unid', validators=[DataRequired()])
    validade = IntegerField('Dias/Validade', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    mixprodutos = FieldList(FormField(MixProdutosForm))
    cliente = SelectField('Cliente/Fábrica Relacionada', coerce=int)

    submit = SubmitField('Cadastrar Receita')

    def __int__(self):
        super(ReceitaForm, self).__init__()
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

    def to_dict(self):  # metodo personalizado no seu formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
        return {
            'descricao_mix': self.descricao_mix.data,
            'modo_preparo': self.modo_preparo.data,
            'departamento': self.departamento.data,
            'rend_kg': self.rend_kg.data,
            'rend_unid': self.rend_unid.data,
            'validade': self.validade.data,
            'status': self.status.data,
            'mixprodutos': [mixproduto.to_dict() for mixproduto in self.mixprodutos.entries],
            'cliente': self.cliente.data,
        }


@app.route('/receitas/formulario', methods=['GET', 'POST'])
def exibir_formreceita():
    form = ReceitaForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            cliente_id = form_data['cliente']
            mixprodutos = form_data['mixprodutos']
            cliente = cliente_service.listar_cliente_id(cliente_id)
            if cliente is None:
                raise ValidationError(f"O cliente com id {cliente_id} não foi encontrado.")
            else:
                form_data['cliente'] = cliente
                receita = Receita(**form_data)
                for mixproduto_data in mixprodutos:
                    produto_id = mixproduto_data['produto']
                    quantidade = mixproduto_data['quantidade']
                    produto = Produto.query.get(produto_id)
                    if produto:
                        mixproduto = MixProduto(produto=produto, quantidade=quantidade, receita=receita)
                        form_data['mixprodutos'].append(mixproduto)
                    else:
                        raise ValidationError(f"O produto com id {produto_id} não foi encontrado.")

                db.session.add(receita)
                db.session.commit()
                flash('Receita cadastrada com sucesso!')
                return redirect(url_for('listar_receitas'))
        except ValidationError as e:
            flash(f"Erro ao cadastrar Receita: {e}")
    return render_template('receitas/formreceita.html', form=form)


@app.route('/receitas/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_receita(id):
    atuareceita = Receita.query.get(id)
    if not atuareceita:
        return render_template("receitas/receitas2.html", error_message="Receita não encontrada"), 404

    form = ReceitaForm(request.form, obj=atuareceita)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(atuareceita)
        for mixproduto_data in form.mixprodutos:
            mixproduto = MixProduto(**mixproduto_data.to_dict())
            atuareceita.mixprodutos.append(mixproduto)

        db.session.add(atuareceita)
        db.session.commit()
        flash('Receita atualizada com sucesso!')
        return redirect(url_for('listar_receitas'))

    return render_template('receitas/formreceita.html', form=form, receita=atuareceita)


@app.route('/receitas/cadastrar_receita', methods=['GET', 'POST'])
def cadastrar_receita():
    form = ReceitaForm()
    if request.method == 'POST' and form.validate_on_submit():

        nova_receita = Receita(
            descricao_mix=form.descricao_mix.data, modo_preparo=form.modo_preparo.data,
            departamento=form.departamento.data, rend_kg=form.rend_kg.data, rend_unid=form.rend_unid.data,
            validade=form.validade.data, status=form.status.data, clientes=form.clientes.data
        )

        for mix_produto_form in form.mixprodutos:
            produto_id = mix_produto_form.produto.data
            quantidade = mix_produto_form.quantidade.data
            produto = Produto.query.get(produto_id)
            if not produto:
                raise ValueError(f"O produto com id {produto_id} não foi encontrado.")

            mixprodutos = MixProduto(produto=produto, quantidade=quantidade, receita=nova_receita)
            db.session.add(mixprodutos)

        db.session.add(nova_receita)
        db.session.commit()
        flash('Receita cadastrada com sucesso!')
        return redirect(url_for('listar_receitas'))
    return render_template('receitas/formreceita.html', form=form)

##
@app.route('/adicionar_produtos/<int:receita_id>', methods=['GET', 'POST'])
def adicionar_produtos(receita_id):
    receita = Receita.query.get(receita_id)

    if request.method == "POST":
        produto_id = request.form.get('produto_id')
        quantidade = request.form.get('quantidade')
        produto = Produto.query.get(produto_id)
        if not produto:
            raise ValueError(f"O produto com id {produto_id} não foi encontrado.")

        mix_produto = MixProduto(produto=produto, quantidade=quantidade, receita=receita)

        # Adicione o produto ao mix de produtos da receita.
        receita.mixprodutos.append(produto)

        db.session.add(mix_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!')
        return render_template('receitas/formreceita.html', receita=receita, receita_id=receita_id)
    produtos = Produto.query.all()

    return render_template('receitas/adicionar_produtos.html', receita=receita, produtos=produtos, receita_id=receita_id)


@app.route('/adicionar_produto/<int:receita_id>', methods=['GET', 'POST'])
def adicionar_produto(receita_id):
    receita = Receita.query.get(receita_id)
    form = MixProdutosForm(request.form)

    if request.method == 'POST' and form.validate():
        produto = form.produto.data
        quantidade = form.quantidade.data

        mix_produto = MixProduto(produto=produto, quantidade=quantidade, receita=receita)
        db.session.add(mix_produto)
        db.session.commit()

    return render_template('receitas/adicionar_produtos.html', form=form, receita=receita, receita_id=receita_id)

@app.route('/receita/<int:receita_id>/produtos', methods=['GET'])
def produtos_da_receita(receita_id):
    receita = Receita.query.get(receita_id)
    mix_produtos = receita.mix_produtos
    return render_template('produtos_da_receita.html', receita=receita, mix_produtos=mix_produtos)

@app.route('/receita/<int:receita_id>/atualizarprodutos', methods=['GET', 'POST'])
def atualizar_produtos_da_receita(receita_id):
    receita = Receita.query.get(receita_id)
    form = MixProdutosForm(request.form)

    if request.method == 'POST' and form.validate():
        produto = form.produto.data
        quantidade = form.quantidade.data

        mix_produto = MixProduto(produto=produto, quantidade=quantidade, receita=receita)
        db.session.add(mix_produto)
        db.session.commit()

    return render_template('produtos_da_receita.html', receita=receita, form=form)


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
        return render_template("receitas/receitas2.html", receitas=receitas)

        ##return jsonify(receita_schema.ReceitaSchema(many=True).dump(receitas))


@app.route('/receitas/<int:id>', methods=['GET', 'POST'])
def visualizar_receita(id):
    receita = receita_service.listar_receita_id(id)
    if not receita:
        return render_template("receitas/receitas2.html", error_message="Receita não encontrada"), 404
    else:
        receita_data = receita_schema.ReceitaSchema().dump(receita)
        # Obter o nome do Cliente/Fabrica
        cliente = receita.cliente
        cliente_nome = cliente.nome if cliente else 'Cliente/Fabrica não encontrado'
        receita_data['cliente'] = cliente_nome

        # Obter o Produto
        mixprodutos = receita.mixprodutos
        produtos_quantidades = []
        for mixproduto in mixprodutos:
            receita_id = mixproduto.receita.id
            produto_id = mixproduto.produto
            quantidade = mixproduto.quantidade
            produtos_quantidades.append({
                'receita_id': receita_id,
                'produto_id': produto_id.id,
                'quantidade': quantidade
            })

            return render_template('receitas/detalhes.html', receita=receita_data, produtos_quantidades=produtos_quantidades, mixprodutos=mixprodutos)
        else:
            # Caso o pedido não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Receita não encontrada', status_code=404)


@app.route('/receitas/<int:id>', methods=['GET', 'POST'])
def visualizar_receita222(id):
    receita = receita_service.listar_receita_id(id)
    if not receita:
        return render_template("receitas/receitas2.html", error_message="Receita não encontrada"), 404

    if request.method == 'GET':
        receita_data = receita_schema.ReceitaSchema().dump(receita)
        # Obter o nome do Cliente/Fabrica
        cliente = receita.clientes
        cliente_nome = cliente.nome if cliente else 'Cliente/Fabrica não encontrado'
        receita_data['clientes'] = cliente_nome

        # Obter o Produto
        mixprodutos = receita.mixprodutos
        produtos_quantidades = []
        for mixproduto in mixprodutos:
            receita_id = mixproduto.receita.id
            produto_id = mixproduto.produto
            quantidade = mixproduto.quantidade
            produtos_quantidades.append({
                'receita_id': receita_id,
                'produto_id': produto_id.id,
                'quantidade': quantidade
            })

            return render_template('receitas/detalhes.html', receita=receita_data, produtos_quantidades=produtos_quantidades, mixprodutos=mixprodutos)
        else:
            # Caso o pedido não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Receita não encontrada', status_code=404)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            receita = receita_service.listar_receita_id(id)
            if receita:
                receita_service.remove_receita(receita)
                return redirect(url_for('listar_receitas'))

            return render_template('error.html', message='Receita não encontrada', status_code=404)
        return render_template('error.html', message='Método não permitido', status_code=405)
    return render_template('receitas/detalhes.html', receita=receita)


@app.route('/receitas/<int:id>/deletar', methods=['DELETE'])
def deletar_receita(id):
    receita = receita_service.listar_receita_id(id)
    if receita:
        db.session.delete(receita)
        db.session.commit()
    return redirect(url_for('listar_receitas'))
