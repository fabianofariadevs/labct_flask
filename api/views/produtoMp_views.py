from flask import render_template, url_for, request, redirect, flash
from sqlalchemy.exc import IntegrityError
from ..models.produtoMp_model import Inventario, Produto
from ..models.estoque_model import Estoque
from api import api, app, db
from ..services import produtoMp_service
from ..schemas import produtoMp_schema, fornecedor_schemas, estoque_schema
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
    #status = BooleanField('Status')
    fornecedor_id = SelectField('Fornecedor(s)', validators=[DataRequired()])
    #cliente_id = SelectField('Cliente/Fabrica')

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fornecedor_id.choices = [(fornecedor.id, fornecedor.nome)
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
            'fornecedor_id': self.fornecedor_id.data,
            #'cliente_id': self.cliente_id.data,
        }
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

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    if request.method == 'GET':
        produtos = produtoMp_service.listar_produtos()
        produtos_data = produtoMp_schema.ProdutoMpSchema().dump(produtos, many=True)
        total_produtos = len(produtos)
        total_produtos_ativos = len([produto for produto in produtos if produto.status == 1])
        total_produtos_inativos = len([produto for produto in produtos if produto.status == 0])

        return render_template("produtos/produtos.html", produtos=produtos_data, total_produtos=total_produtos,
                           total_produtos_ativos=total_produtos_ativos,
                           total_produtos_inativos=total_produtos_inativos)


@app.route('/produtos/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_produto(id):
    produto = produtoMp_service.listar_produto_id(id)
    if not produto:
        return render_template("produtos/produtos.html", error_message="Cliente não encontrado"), 404

    form = ProdutoForm(obj=produto)
    if form.validate_on_submit():
        produto_atualizado = Produto.query.get(id)
        form.populate_obj(produto_atualizado)
        produtoMp_service.atualiza_produto(produto, produto_atualizado)
        return redirect(url_for("listar_produtos"))

    return render_template("produtos/formproduto.html", produto=produto, form=form), 400


@app.route('/produtos/formulario', methods=['GET', 'POST'])
def exibir_formproduto():
    form = ProdutoForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            produto = produtoMp_schema.ProdutoMpSchema().load(form_data)
            produto_bd = produtoMp_service.cadastrar_produto(produto)
            produto_data = produtoMp_schema.ProdutoMpSchema().dump(produto_bd)
            flash("Produto cadastrado com sucesso!")
            return redirect(url_for("listar_produtos"))
        except ValidationError as error:
            flash("Erro ao cadastrar Produto")
    return render_template('produtos/formproduto.html', form=form)

@app.route('/produtos/<int:id>/deletar', methods=['DELETE'])
def deletar_produto(id):
    produto = produtoMp_service.listar_produto_id(id)
    if deletar_produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect(url_for('listar_produtos'))



####NOVO MODELSSS VERR
@app.route('/produt', methods=['GET'])
def produtose():
    produtos = estoque_schema.query.order_by(estoque_schema.nome).all()
    return render_template('produtos/novo_produto.html', produtos=produtos)


@app.route('/produtos_faltando')
def produtos_faltando():
    produtos = Estoque.query.order_by(Estoque.nome).all()
    produtos_em_falta = []

    for produto in produtos:
        if int(produto.quantidade_estoque) < int(produto.quantidade_minima):
            produtos_em_falta.append(produto)

    return render_template('produtos/produtos_faltando.html', produtos=produtos_em_falta)


@app.route('/criar_produto', methods=['POST'])
def criar_produto():
    nome = request.form['nome']
    valor_compra = request.form['valor_compra']
    valor_venda = request.form['valor_venda']
    quantidade_estoque = request.form['quantidade_estoque']
    quantidade_minima = request.form['quantidade_minima']

    novo_produto = Estoque(
        nome=nome, valor_compra=valor_compra, valor_venda=valor_venda,
        quantidade_estoque=quantidade_estoque, quantidade_minima=quantidade_minima)
    try:
        db.session.add(novo_produto)
        db.session.commit()
    except IntegrityError:
        return redirect(url_for('novo_produto', erro_nome='sim'))
    return redirect(url_for('produtos'))


@app.route('/alterar_produto/<id>')
def alterar_produto(id):
    produto_para_modificar = Estoque.query.filter_by(id=id).first()
    return render_template('listar_produtos.html', produto=produto_para_modificar)


@app.route('/modificar', methods=['POST'])
def modificar():
    id = request.form['id']
    produto_para_modificar = Estoque.query.filter_by(id=id).first()
    produto_para_modificar.nome = request.form['nome']
    produto_para_modificar.valor_compra = request.form['valor_compra']
    produto_para_modificar.valor_venda = request.form['valor_venda']
    produto_para_modificar.quantidade_estoque = request.form['quantidade_estoque']
    produto_para_modificar.quantidade_minima = request.form['quantidade_minima']

    db.session.add(produto_para_modificar)
    db.session.commit()

    return redirect(url_for('produtos'))


@app.route('/excluir_produto/<id>')
def excluir_produto(id):
    produto_para_remover = Estoque.query.filter_by(id=id).first()
    db.session.delete(produto_para_remover)
    db.session.commit()
    return redirect(url_for('produtos'))


@app.route('/venda')
def venda():
    produtos = Estoque.query.all()
    return render_template('produtos/venda.html', produtos=produtos)


@app.route('/finalizar_venda', methods=['POST'])
def finalizar_venda():
    lista_venda = request.form['lista_de_itens'].split(',')
    for elemento in lista_venda:
        if elemento == '':
            lista_venda.remove(elemento)

    # [produto] = nome do produto, [produto+1] = quantidade vendida do produto...
    for produto in range(0, len(lista_venda), 2):
        produto_para_vender = Estoque.query.filter_by(nome=lista_venda[produto]).first()
        if produto_para_vender is not None:
            if int(produto_para_vender.quantidade_estoque) >= int(lista_venda[produto + 1]):
                produto_para_vender.quantidade_estoque = str(
                    int(produto_para_vender.quantidade_estoque) - int(lista_venda[produto + 1]))
                db.session.add(produto_para_vender)
                db.session.commit()

    return redirect(url_for('produtos'))


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

