from api import api, app, db
from flask import render_template, url_for, request, redirect, flash
from ..models.produtoMp_model import Inventario, Produto
from ..models.estoque_model import Estoque
from ..services import produtoMp_service
from ..schemas import produtoMp_schema, estoque_schema
from ..models.fornecedor_model import Fornecedor
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError

class ProdutoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    descricao = StringField("Descrição", validators=[DataRequired()])
    quantidade = StringField('Qtde', validators=[DataRequired()])
    compra_unid = StringField('Compra_unid', validators=[DataRequired()])
    peso_pcte = StringField('Peso_pcte', validators=[DataRequired()])
    valor = StringField('Valor R$', validators=[DataRequired()])
    custo_ultima_compra = StringField('custo_ult_compra', validators=[DataRequired()])
    whatsapp = StringField('Whatsapp', validators=[DataRequired()])
    qrcode = StringField('Qrcode')
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    fornecedor = SelectField('Fornecedor(s)', validators=[DataRequired()], coerce=int)
    estoque_minimo = StringField('Estoque_minimo', validators=[DataRequired()])
    obs = StringField('Obs')

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fornecedor.choices = [(fornecedor.id, fornecedor.nome)
                                   for fornecedor in Fornecedor.query.all()]

        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    def to_dict(self):  # metodo personalizado no seu formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
        return {
            'nome': self.nome.data,
            'descricao': self.descricao.data,
            'quantidade': self.quantidade.data,
            'compra_unid': self.compra_unid.data,
            'peso_pcte': self.peso_pcte.data,
            'valor': self.valor.data,
            'custo_ultima_compra': self.custo_ultima_compra.data,
            'whatsapp': self.whatsapp.data,
            'qrcode': self.qrcode.data,
            'status': self.status.data,
            'fornecedor': int(self.fornecedor.data) if self.fornecedor.data else None,
            'estoque_minimo': self.estoque_minimo.data,
            'obs': self.obs.data,
        }

@app.route('/produtos/buscar', methods=['GET'])
def buscar_produto():
    nome_produto = request.args.get('nome_produto', '').strip().lower()
    resultados = None

    if nome_produto:
        # Lógica para buscar o produto por nome
        produtos = produtoMp_service.listar_produtos()
        resultados = [produto for produto in produtos if nome_produto in produto.nome.lower()]

    return render_template("produtos/consultar_produtos.html", resultados=resultados, nome_produto=nome_produto)


@app.route('/produtos/<int:id>', methods=['GET', 'POST'])
def visualizar_produto(id):
    if request.method == 'GET':
        produto = produtoMp_service.listar_produto_id(id)
        return render_template('produtos/detalhes.html', produto=produto)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            produto = produtoMp_service.listar_produto_id(id)
            if produto:
                produtoMp_service.remove_produto(produto)
                return redirect(url_for('listar_produtos'))

        return redirect(url_for('listar_produtos'))


@app.route('/produtos/<int:id>/inventario', methods=['GET', 'POST'])
def visualizar_inventario(id):
    if request.method == 'GET':
        produto = produtoMp_service.listar_produto_id(id)
        return render_template('produtos/detalhes.html', produto=produto)

    elif request.method == 'POST':
        inventario = Inventario()
        inventario.produto_id = id
        inventario.quantidade = request.form['quantidade']
        inventario.nome = request.form['nome']
        inventario.descricao = request.form['descricao']
        inventario.detalhes = request.form['detalhes']
        inventario.obs = request.form['obs']
        inventario.data = request.form['data']
        db.session.add(inventario)
        db.session.commit()
        return redirect(url_for('listar_inventario'))

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    if request.method == 'GET':
        produtos = produtoMp_service.listar_produtos()

        return render_template("produtos/produtos.html", produtos=produtos)

@app.route('/produtos', methods=['GET'])
def listar_produtos9999():
    if request.method == 'GET':
        produtos = produtoMp_service.listar_produtos()
        produtos_data = produtoMp_schema.ProdutoMpSchema(many=True).dump(produtos)
        total_produtos = len(produtos)
        total_produtos_ativos = len([produto for produto in produtos if produto.status == 1])
        total_produtos_inativos = len([produto for produto in produtos if produto.status == 0])

        return render_template("produtos/produtos.html", produtos=produtos_data, total_produtos=total_produtos,
                               total_produtos_ativos=total_produtos_ativos,
                               total_produtos_inativos=total_produtos_inativos)

@app.route('/produtos/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_produto(id):
    produto = produtoMp_service.listar_produto_id(id)
    form = ProdutoForm(obj=produto)

    if request.method == 'POST' and form.validate_on_submit():
        form_data = form.to_dict()
        fornecedor_id = form_data['fornecedor']
        produto_novo = produtoMp_service.atualiza_produto(form_data, produto, fornecedor_id)
        flash("Produto atualizado com sucesso!")
        return redirect(url_for("listar_produtos"))
    return render_template('produtos/formproduto.html', form=form, produto=produto)


@app.route('/produtos/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_produto999(id):
    produto = produtoMp_service.listar_produto_id(id)
    if not produto:
        return render_template("produtos/produtos.html", error_message="Produto não encontrado"), 404

    form = ProdutoForm(obj=produto)
    if form.validate_on_submit():
        form_data = form.to_dict()
        produto_novo = produtoMp_schema.ProdutoMpSchema().load(form_data)
        produtoMp_service.atualiza_produto(produto, produto_novo)
        return redirect(url_for("listar_produtos"))

    return render_template('produtos/formproduto.html', form=form)


@app.route('/produtos/formulario', methods=['GET', 'POST'])
def exibir_formproduto():
    form = ProdutoForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            fornecedor_id = form_data['fornecedor']
            fornecedor = Fornecedor.query.get(fornecedor_id)
            if fornecedor is not None:
                produto_bd = produtoMp_service.cadastrar_produto(form_data)
                flash("Produto cadastrado com sucesso!")
                return redirect(url_for('listar_produtos'))
            else:
                flash("Fornecedor não encontrado!")
                return redirect(url_for('exibir_formproduto')), 400
        except ValidationError as e:
            flash("Erro ao cadastrar Produto!")
            return redirect(url_for('exibir_formproduto')), 400

    return render_template('produtos/formproduto.html', form=form)


@app.route('/produtos/<int:id>/deletar', methods=['DELETE'])
def deletar_produto(id):
    produto = produtoMp_service.listar_produto_id(id)
    if deletar_produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect(url_for('listar_produtos'))


@app.route('/produtos_faltando')
def produtos_faltando():
    produtos = Estoque.query.order_by(Estoque.nome).all()
    produtos_em_falta = []

    for produto in produtos:
        if int(produto.quantidade_estoque) < int(produto.quantidade_minima):
            produtos_em_falta.append(produto)

    return render_template('produtos/produtos_faltando.html', produtos=produtos_em_falta)


@app.route('/reestoque')
def reestoque():
    produtos = Estoque.query.all()
    return render_template('produtos/reestoque.html', produtos=produtos)


@app.route('/compra', methods=['post'])
def compra():
    lista_compra = request.form['lista_de_itens'].split(',')
    for elemento in lista_compra:
        if elemento == '':
            lista_compra.remove(elemento)
    # [produto] = nome do produto, [produto+1] = quantidade adicionada do produto...
    for produto in range(0, len(lista_compra), 2):
        produto_para_adicionar = Estoque.query.filter_by(nome=lista_compra[produto]).first()
        if produto_para_adicionar is not None:
            produto_para_adicionar.quantidade_estoque = str(
                int(lista_compra[produto + 1]) + int(produto_para_adicionar.quantidade_estoque))
            db.session.add(produto_para_adicionar)
            db.session.commit()
    return redirect(url_for('produtos'))


@app.route('/inventario/<int:id>', methods=['GET'])
def visualizar_produo(id):
    produto = produtoMp_service.listar_produto_id(id)
    return render_template('produtos/detalhes.html', produto=produto)

@app.route('/inventario', methods=['GET'])
def listar_inventario():
    if request.method == 'GET':
        inventarios = produtoMp_service.listar_inventarios()
        inventarios_data = produtoMp_schema.InventarioSchema().dump(inventarios, many=True)
        total_inventarios = len(inventarios)
      #  total_inventarios_ativos = len([inventario for inventario in inventarios if inventario.status == True])
       # total_inventarios_inativos = len([inventario for inventario in inventarios if inventario.status == False])

        return render_template("estoque/inventario.html", inventarios=inventarios_data, total_produtos=total_inventarios)

@app.route('/produtos/atencao', methods=['GET'])
def atencao_vencendo():

    return render_template("produtos/atencao.html")
