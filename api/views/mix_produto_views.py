from sqlalchemy.orm import joinedload

from api import app, api, db
from flask import request, make_response, jsonify, render_template, redirect, url_for
from ..models.receita_model import Receita
from ..models.estoque_model import Estoque
from ..models.filial_pdv_model import Filial
from ..services import mix_produto_service
from ..paginate import paginate
from ..models.mix_produto_model import MixProduto, Producao
from ..schemas.receita_schema import ReceitaSchema
from ..schemas.estoque_schema import EstoqueSchema
from ..schemas import mix_produto_schema
from ..models.produtoMp_model import Produto
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError

class MixProdutosForm(FlaskForm):
    cod_prod_mix = StringField('Código do Produto', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    situacao = SelectField('Situação', choices=[("0", 'em Aberto'), ("1", 'em Produção'), ("2", 'Finalizado'), ("3", 'em Distribuição')], validators=[DataRequired()])
    cadastrado_em = StringField('Cadastrado em', validators=[DataRequired()])
    atualizado_em = StringField('Atualizado em', validators=[DataRequired()])
    receita = SelectField('Receita', validators=[DataRequired()], coerce=int)
    produtos = SelectField('Produto', validators=[DataRequired()], coerce=int)
    quantidade = StringField('Quantidade', validators=[DataRequired()])

    submit = SubmitField('CadastrarMixProduto')

    def __init__(self, *args, **kwargs):
        super(MixProdutosForm, self).__init__(*args, **kwargs)
        self.receita.choices = [(receita.id, receita.descricao_mix) for receita in Receita.query.all()]

        self.produtos.choices = [(produto.id, produto.nome) for produto in Produto.query.all()]

        self.situacao.choices = self.get_situacao_choices()

        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    @staticmethod
    def get_situacao_choices():
        return [("0", 'em Aberto'), ("1", 'em Produção'), ("2", 'Finalizado'), ("3", 'em Distribuição')]

    def to_dict(self):
        return {
            "cod_prod_mix": self.cod_prod_mix.data,
            "status": self.status.data,
            "situacao": self.situacao.data,
            "cadastrado_em": self.cadastrado_em.data,
            "atualizado_em": self.atualizado_em.data,
            "receita": self.receita.data,
            "produtos": self.produtos.data,
            "quantidade": self.quantidade.data
        }

@app.route('/mixprodutos', methods=['GET'])
def listar_mixprodutos():
    if request.method == 'GET':
        mixprodutos = MixProduto.query.options(joinedload("receita")).options(joinedload("filiais")).options(joinedload("pedidosprod")).options(joinedload("producoes")).options(joinedload("produtos")).all()
        mixprodutos_data = []
        for mixproduto in mixprodutos:
            mixproduto_dict = mix_produto_schema.MixProdutoSchema().dump(mixproduto)

            receita = mixproduto.receita
            mixproduto_dict['receita'] = receita.descricao_mix if receita else None

            filiais = mixproduto.filiais
            mixproduto_dict['filiais'] = filiais.nome if filiais else None

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
                    "receitas": pedido.receitas,
                    "filiais": pedido.filiais,
                    "cliente": pedido.cliente,
                    "mixprodutos": pedido.mixprodutos,
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

    # Renderize o relatório em uma página HTML (ou qualquer outro formato desejado)
    return render_template('relatorio_estoque.html', estoque=estoque_json)

@app.route('/gerar_relatorio_producao', methods=['GET'])
def gerar_relatorio_producao():
    # Consulte o banco de dados para obter informações sobre a produção de receitas
    # Suponha que você tenha um modelo 'Receita' para representar as receitas e 'MixProduto' para representar o mix de produtos

    receitas = Receita.query.all()

    # Serialize os dados das receitas e do mix de produtos
    receita_schema = ReceitaSchema(many=True)
    receita_json = receita_schema.dump(receitas)

    # Renderize o relatório em uma página HTML (ou qualquer outro formato desejado)
    return render_template('relatorio_producao.html', receitas=receita_json)


@app.route('/ver_mix_produto/<int:receita_id>')
def ver_mix_produto(receita_id):
    receita = Receita.query.get(receita_id)
    mix_produtos = MixProduto.query.filter_by(receita_id=receita_id).all()
    return render_template('ver_mix_produto.html', receita=receita, mix_produtos=mix_produtos)

@app.route('/adicionar_produtos/<int:receita_id>', methods=['GET', 'POST'])
def adicionar_mixprodutos99(receita_id):
    receita = Receita.query.get(receita_id)

    if request.method == 'POST':
        produto_id = request.form.get('produto_id')  # Este é um exemplo; ajuste de acordo com seu formulário.
        produto = Produto.query.get(produto_id)

        # Adicione o produto ao mix de produtos da receita.
        receita.produtos_receita.append(produto)

        db.session.commit()
        return redirect(url_for('ver_receita', receita_id=receita_id))  # Redirecionar para a visualização da receita após a adição.

    produtos = Produto.query.all()
    return render_template('adicionar_produtos.html', receita=receita, produtos=produtos)

@app.route('/adicionar_mixproduto/<int:receita_id>', methods=['GET', 'POST'])
def adicionar_mixproduto(receita_id):
    receita = Receita.query.get(receita_id)
    form = MixProdutosForm(request.form)
    if request.method == 'POST' and form.validate():
        mix_produto = MixProduto(**form.to_dict())
        db.session.add(mix_produto)
        db.session.commit()
        return render_template('mix_produto/ver_mix_produto.html', receita=receita, mix_produtos=mix_produto)
    return render_template('adicionar_mixproduto.html', form=form, receita=receita)


@app.route("/mixprodutos", methods=["GET"])
def listar_mixprodutos22():
    mixprodutos = mix_produto_service.listar_mixprodutos()
    #return jsonify(mix_produto_schema.MixprodutoSchema(many=True).dump(mixprodutos))
    return render_template('mix_produto/mixprodutos.html', mixprodutos=mixprodutos)

@app.route("/mixprodutos/<int:id>", methods=["GET"])
def localizar_mixproduto(id: int):
    mixproduto = mix_produto_service.listar_mixproduto_id(id)
    return jsonify(mix_produto_schema.MixProdutoSchema().dump(mixproduto))

@app.route("/mixprodutos/<int:id>", methods=["PUT"])
def atualizar_mixproduto(id: int):
    schema = mix_produto_schema.MixProdutoSchema()
    mixproduto = schema.load(request.json)
    mix_produto_service.atualizar_mixproduto(mixproduto, id)
    return jsonify(schema.dump(mixproduto))

