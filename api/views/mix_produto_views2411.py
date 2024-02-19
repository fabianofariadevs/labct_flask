from sqlalchemy.orm import joinedload
from api import app, api, db
from flask import request, make_response, jsonify, render_template, redirect, url_for, flash
from ..models.receita_model import Receita
from ..models.estoque_model import Estoque
from ..services import mix_produto_service
from ..schemas.receita_schema import ReceitaSchema
from ..schemas.estoque_schema import EstoqueSchema
from ..schemas import mix_produto_schema
from ..models.produtoMp_model import Produto, mixproduto_produto
from ..models.mix_produto_model import MixProduto, QuantidadeMixProdutos
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, SelectMultipleField, FloatField, FieldList
from datetime import datetime
from wtforms.validators import DataRequired, ValidationError
from ..paginate import paginate

class MixProdutosForm(FlaskForm):
    cod_prod_mix = StringField('Cód. MixProd', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    receita = SelectField('Receita', validators=[DataRequired()], coerce=int)
    produtos = SelectMultipleField('Produtos', validators=[DataRequired()], coerce=int)
    quantidades = FieldList(FloatField('Quantidade', render_kw={"placeholder": "Quantidade para cada produto"}), min_entries=1)

    submit = SubmitField('CadastrarMixProduto')

    def __init__(self, *args, **kwargs):
        super(MixProdutosForm, self).__init__(*args, **kwargs)
        self.receita.choices = [(receita.id, receita.descricao_mix) for receita in Receita.query.all()]

        self.produtos.choices = [(produto.id, produto.nome) for produto in Produto.query.all()]

        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    def to_dict(self):
        return {
            "cod_prod_mix": self.cod_prod_mix.data,
            "status": self.status.data,
            "receita": int(self.receita.data) if self.receita.data else None,
            "produtos": int(self.produtos.data) if self.produtos.data else None,
            "quantidades": self.quantidades.data,
        }

@app.route('/mixprodutos', methods=['GET'])
def listar_mixprodutos():
    if request.method == 'GET':
        mixprodutos = mix_produto_service.listar_mixprodutos()
        return render_template('mix_produto/mixproduto.html', mixprodutos=mixprodutos)

@app.route('/mixprodutos1', methods=['GET'])
def listar_mixprodutos1():
    if request.method == 'GET':
        #mixprodutos = MixProduto.query.options(joinedload("receita")).options(joinedload("pedidosprod")).options(joinedload("producoes")).options(joinedload("produtos")).all()
        mixprodutos = MixProduto.query.options(joinedload("receita")).all()
        mixprodutos_data = []
        for mixproduto in mixprodutos:
            mixproduto_dict = mix_produto_schema.MixProdutoSchema().dump(mixproduto)

            receita = mixproduto.receita
            mixproduto_dict['receita'] = receita.descricao_mix if receita else None

            pedidosprod = mixproduto.pedidosprod

            # Ajuste para lidar com a lista de pedidosprod
            pedidosprod_data = []
            for pedido in pedidosprod:
                pedidosprod_data.append({
                    "data_pedido": pedido.data_pedido if pedido.data_pedido else None,
                    "data_entrega": pedido.data_entrega if pedido.data_entrega else None,
                    "qtde_pedido": pedido.qtde_pedido if pedido.qtde_pedido else None,
                    "status": pedido.status,
                    "obs": pedido.obs,
                    "cadastrado_em": pedido.cadastrado_em,
                    "atualizado_em": pedido.atualizado_em,
                    "cliente": pedido.cliente,
                    "producoes": pedido.producoes if pedido.producoes else None
                })

            mixproduto_dict['pedidosprod'] = pedidosprod_data

            producoes = mixproduto.producoes
            mixproduto_dict['producoes'] = producoes.data_producao if producoes else None

            produtos = mixproduto.produtos
            mixproduto_dict['produtos'] = produtos.nome if produtos else None

            mixprodutos_data.append(mixproduto_dict)

        total_mixprodutos = len(mixprodutos)
        total_mixprodutos_ativos = len([mixproduto for mixproduto in mixprodutos if mixproduto.status == 1])
        total_mixprodutos_inativos = len([mixproduto for mixproduto in mixprodutos if mixproduto.status == 0])

        return render_template('mix_produto/mixproduto.html', mixprodutos=mixprodutos_data, total_mixprodutos=total_mixprodutos,
                               total_mixprodutos_ativos=total_mixprodutos_ativos,
                               total_mixprodutos_inativos=total_mixprodutos_inativos)

@app.route('/gerar_relatorio_estoque', methods=['GET'])
def gerar_relatorio_estoque():
    # Consulte o banco de dados para obter informações sobre o estoque
    # Suponha que você tenha um modelo 'Estoque' para representar o estoque
    estoque_itens = Estoque.query.all()

    # Serialize os dados do estoque para o formato desejado
    estoque_schema = EstoqueSchema(many=True)
    estoque_json = estoque_schema.dump(estoque_itens)

    # Renderize o relatório página HTML (ou qualquer outro formato desejado)
    return render_template('relatorio_estoque.html', estoque=estoque_json)

@app.route('/gerar_relatorio_producao', methods=['GET'])
def gerar_relatorio_producao():
    # Consulte o banco de dados para obter informações sobre a produção de receitas
    # Suponha que você tenha um modelo 'Receita' para representar as receitas e 'MixProduto' para representar o mix de produtos

    receitas = Receita.query.all()

    # Serialize os dados das receitas e do mix de produtos
    receita_schema = ReceitaSchema(many=True)
    receita_json = receita_schema.dump(receitas)

    # Renderize o relatório página HTML (ou qualquer outro formato desejado)
    return render_template('relatorio_producao.html', receitas=receita_json)


@app.route('/ver_mix_produto/<int:receita_id>')
def ver_mix_produto(receita_id):
    receita = Receita.query.get(receita_id)
    mix_produtos = MixProduto.query.filter_by(receita_id=receita_id).all()
    return render_template('ver_mix_produto.html', receita=receita, mix_produtos=mix_produtos)


@app.route('/mixprodutos/formulario', methods=['GET', 'POST'])
def adicionar_mixproduto():
    form = MixProdutosForm()
    if request.method == 'POST' and form.validate_on_submit():
        mix_produto = MixProduto(
            cod_prod_mix=form.cod_prod_mix.data,
            status=form.status.data,
            receita_id=form.receita.data,
            cadastrado_em=datetime.now(),
        )
        receita = Receita.query.get(form.receita.data)
        mix_produto.receita = receita

        try:
            for produto_id, quantidade in zip(form.produtos.data, form.quantidades.data):
                produto = Produto.query.get(produto_id)
                mix_produto.quantidades.append(QuantidadeMixProdutos(produto=produto, quantidade=quantidade))

            db.session.add(mix_produto)
            db.session.commit()

            flash("MixProduto cadastrado com sucesso!")
            return redirect(url_for("listar_mixprodutos"))
        except ValidationError as error:
            flash("Erro ao cadastrar MixProduto")
    return render_template('mix_produto/formmixproduto.html', form=form, mix_produto={})


@app.route('/mixprodutos/<int:id>/', methods=['GET', 'POST'])
def visualizar_mixproduto(id):
    mixproduto = mix_produto_service.listar_mixproduto_id(id)
    if not mixproduto:
        return render_template("mix_produto/mixproduto.html", error_message="MixProduto não encontrado"), 404

    if request.method == 'GET':
        mixproduto_data = mix_produto_schema.MixProdutoSchema().dump(mixproduto)

        receita = mixproduto.receita
        mixproduto_data['receita'] = receita.descricao_mix if receita else None

        pedidosprod = mixproduto.pedidosprod

        # Ajuste para lidar com a lista de pedidosprod
        pedidosprod_data = []
        for pedido in pedidosprod:
            pedidosprod_data.append({
                "data_pedido": pedido.data_pedido if pedido.data_pedido else None,
                "data_entrega": pedido.data_entrega if pedido.data_entrega else None,
                "qtde_pedido": pedido.qtde_pedido if pedido.qtde_pedido else None,
                "status": pedido.status,
                "obs": pedido.obs,
                "cadastrado_em": pedido.cadastrado_em,
                "atualizado_em": pedido.atualizado_em,
                "filiais": pedido.filiais if pedido.filiais else None,
                "cliente": pedido.cliente,
                "mixprodutos": pedido.mixprodutos if pedido.mixprodutos else None,
                "producoes": pedido.producoes if pedido.producoes else None
            })

        mixproduto_data['pedidosprod'] = pedidosprod_data

        producoes = mixproduto.producoes
        mixproduto_data['producoes'] = producoes.data_producao if producoes else None

      #  produtos = mixproduto.produtos
       # mixproduto_data['produtos'] = produtos.nome if produtos else None

        return render_template('mix_produto/detalhes.html', mixproduto=mixproduto_data)

    elif request.method == 'POST':
        if request.form.get('_method') == 'DELETE':
            mixproduto = mix_produto_service.listar_mixproduto_id(id)
            if mixproduto:
                mix_produto_service.deletar_mixproduto(mixproduto)
                return redirect(url_for('listar_mixprodutos'))


@app.route('/mixprodutos/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_mixproduto(id):
    mixproduto = mix_produto_service.listar_mixproduto_id(id)
    if not mixproduto:
        return render_template("mix_produto/mixproduto.html", error_message="MixProduto não encontrado"), 404

    form = MixProdutosForm(obj=mixproduto)
    if form.validate_on_submit():
        mixproduto_atualizado = MixProduto.query.get(id)
        form.populate_obj(mixproduto_atualizado)
        mix_produto_service.atualizar_mixproduto(mixproduto, mixproduto_atualizado)
        return redirect(url_for("listar_mixprodutos"))

    return render_template("mix_produto/formmixproduto.html", mixproduto=mixproduto, form=form), 400

