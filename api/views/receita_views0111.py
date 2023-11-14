from api import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField, FloatField, FieldList, FormField, Form, IntegerField, TextAreaField
from wtforms.fields import SelectMultipleField
from wtforms.csrf.session import SessionCSRF
from wtforms.csrf.core import CSRF
from flask_wtf.csrf import CSRFProtect

from wtforms_components import SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, length
from ..schemas import receita_schema
from flask import request, make_response, jsonify, render_template, redirect, url_for, flash, session
from ..services import receita_service
from ..models.receita_model import Receita
from ..paginate import paginate
from ..models.mix_produto_model import MixProduto
from ..models.produtoMp_model import Produto
from ..models.filial_pdv_model import Filial
from ..models.cliente_model import Cliente
from sqlalchemy.orm import joinedload
csrf = CSRFProtect(app)
csrf.init_app(app)


class MixProdutoForm(FlaskForm):
    produto = SelectField('Produto', validators=[DataRequired()])
    quantidade = FloatField('Quantidade', validators=[DataRequired()])
    submit = SubmitField('Adicionar Produto')

    def __init__(self, *args, **kwargs):
        super(MixProdutoForm, self).__init__(*args, **kwargs)
        self.produto.choices = [(produto.id, produto.nome)
                                for produto in Produto.query.all()]

    def to_dict(self):
        return {
            'produto': self.produto.data,
            'quantidade': self.quantidade.data
        }

class ReceitaForm(FlaskForm):
    descricao_mix = StringField("Descricao_mix", validators=[DataRequired()])
    modo_preparo = TextAreaField("Modo_preparo", validators=[DataRequired()])
    departamento = StringField('Departamento', validators=[DataRequired()])
    rend_kg = FloatField('Rend_kg', validators=[DataRequired()])
    rend_unid = FloatField('Rend_unid', validators=[DataRequired()])
    validade = SelectField('Validade', choices=[("10", '10 dias'), ("20", '20 dias'), ("30", '30 dias')], validators=[DataRequired()], coerce=int)
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    mix_produtos = FieldList(FormField(MixProdutoForm), min_entries=1)
    clientes = SelectField('Cliente/Fábrica Relacionada', coerce=int)

    submit = SubmitField('Cadastrar Receita')

    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        self.clientes.choices = [(cliente.id, cliente.nome)
                                 for cliente in Cliente.query.all()]

        self.mix_produtos.append_entry(
            MixProdutoForm(produto=None, quantidade=None)
        )

        self.validade.choices = self.get_validade_choices()

        self.status.choices = self.get_status_choices()

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
            'mix_produtos': [mix_produto.to_dict() for mix_produto in self.mix_produtos],
            #'filiais': self.filiais.data,
            'clientes': self.clientes.data,
        }

    def populate_obj(self, obj):
        obj.descricao_mix = self.descricao_mix.data
        obj.modo_preparo = self.modo_preparo.data
        obj.departamento = self.departamento.data
        obj.rend_kg = self.rend_kg.data
        obj.rend_unid = self.rend_unid.data
        obj.validade = self.validade.data
        obj.status = self.status.data
        obj.mix_produtos = self.mix_produtos.data
        #obj.filiais = self.filiais.data
        obj.clientes = self.clientes.data

    def validate_descricao_mix(self, field):
        if len(field.data) < 7:
            raise ValidationError('A descrição deve ter mais de 7 caracteres.')

# myapp/app.py

@app.route('/receita/<int:receita_id>', methods=['GET'])
def detalhe9_receita(receita_id):
    receita = Receita.query.get(receita_id)
    mix_produtos = receita.mix_produtos
    form = MixProdutoForm(request.form)

    return render_template('receitas/detalhes.html', receita=receita,form=form , mix_produtos=mix_produtos)

@app.route('/receita/<int:id>', methods=['GET', 'POST'])
def detalhes_receita(id):
    receita = Receita.query.get(id)
    form = MixProdutoForm(request.form)

    if request.method == 'POST' and form.validate():
        produto = form.produto.data
        quantidade = form.quantidade.data

        mix_produto = MixProduto(produto=produto, quantidade=quantidade, receita=receita)
        db.session.add(mix_produto)
        db.session.commit()

    return render_template('receitas/detalhes_receita.html', receita=receita, form=form)

@app.route('/receitas/cadastrar_receita', methods=['GET', 'POST'])
def cadastrar_receita():
    form = ReceitaForm(request.form)

    if request.method == 'POST' and form.validate():
        form_data = form.to_dict()  # Obter os dados do formulário como um dicionário
        mix_produtos = form_data.pop('mix_produtos')  # Obter os produtos da receita
        receita_bd, mix_produtos_bd = receita_service.cadastrar_receita(form_data, mix_produtos)
        flash(f"Receita '{receita_bd.descricao_mix}' cadastrada com sucesso!")

        return redirect(url_for('listar_receitas'))

    return render_template('receitas/cadastrar_receita.html', form=form, action="Cadastrar Receita")

##
@app.route('/adicionar_produto/<int:receita_id>', methods=['GET', 'POST'])
def adicionar_produto(receita_id):
    receita = Receita.query.get(receita_id)
    form = MixProdutoForm(request.form)

    if request.method == 'POST' and form.validate():
        produto = form.produto.data
        quantidade = form.quantidade.data

        mix_produto = MixProduto(produto=produto, quantidade=quantidade, receita=receita)
        db.session.add(mix_produto)
        db.session.commit()

    return render_template('adicionar_mixproduto.html', form=form, receita=receita)

@app.route('/receita/<int:receita_id>/produtos', methods=['GET'])
def produtos_da_receita(receita_id):
    receita = Receita.query.get(receita_id)
    mix_produtos = receita.mix_produtos
    return render_template('produtos_da_receita.html', receita=receita, mix_produtos=mix_produtos)

@app.route('/receita/<int:receita_id>/atualizarprodutos', methods=['GET', 'POST'])
def atualizar_produtos_da_receita(receita_id):
    receita = Receita.query.get(receita_id)
    form = MixProdutoForm(request.form)

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

        return render_template('receitas/receitas2.html', receitas=receitas)

@app.route('/receitas', methods=['GET'])
def listar_recei():
    if request.method == 'GET':
        receitas = receita_service.listar_receitas()
        receitas_data = receita_schema.ReceitaSchema(many=True).dump(receitas)

        total_receitas = len(receitas)
        total_receitas_ativos = len([receita for receita in receitas if receita.status == 1])
        total_receitas_inativos = len([receita for receita in receitas if receita.status == 0])

        return render_template("receitas/listar_receitas.html", receitas=receitas_data, total_receitas=total_receitas,
                               total_receitas_ativos=total_receitas_ativos,
                               total_receitas_inativos=total_receitas_inativos)


@app.route('/receitas/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_receita(id):
    atuareceita = receita_service.listar_receita_id(id)
    if not atuareceita:
        return render_template("receitas/receitas2.html", error_message="Receita não encontrada"), 404

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
