from api import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField, FloatField, FieldList, FormField, Form, IntegerField
from wtforms.fields import SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, length
from ..schemas import receita_schema
from flask import request, make_response, jsonify, render_template, redirect, url_for, flash
from ..services import receita_service
from ..models.receita_model import Receita
from ..paginate import paginate
from ..models.produtoMp_model import Produto
from ..models.filial_pdv_model import Filial
from sqlalchemy.orm import joinedload

class ReceitaForm(FlaskForm):
    descricao_mix = StringField("Descricao_mix", validators=[DataRequired()])
    modo_preparo = StringField("Modo_preparo", validators=[DataRequired()])
    departamento = StringField('Departamento', validators=[DataRequired()])
    rend_kg = FloatField('Rend_kg', validators=[DataRequired()])
    rend_unid = FloatField('Rend_unid', validators=[DataRequired()])
    validade = DateField('Validade', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
#    atualizado_em = DateField('atualizado_em', format='%d/%m/%Y')
    produto_id = SelectMultipleField('Produtos', validators=[DataRequired()])
    quantidades = IntegerField('Quantidades', default=1, validators=[DataRequired()])
    produtos = SelectMultipleField('Produtos', validators=[DataRequired()])
    #filial = StringField('Filial Relacionada', validators=[DataRequired()])
   # pedidoprod = StringField('Pedido de Produção', validators=[DataRequired()])
    #produtos = [(1, 'Produto 1'), (2, 'Produto 2')]  # Exemplo de produtos

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        self.produto_id.choices = [(produto.id, produto.nome)
                                   for produto in Produto.query.all()]

        self.produtos.choices = [(produto.id, produto.nome)
                                 for produto in Produto.query.all()]

        # Adicionar opções para quantidades, por exemplo, de 1 a 10
        self.quantidades.choices = [(i, str(i)) for i in range(1, 21)]  # Altere o intervalo conforme necessário
      #  self.filial.choices = [(filial.id, filial.nome) for filial in Filial.query.all()]
       # self.pedidoprod.choices = [(pedidoproducao.id, pedidoproducao.receitas) for pedidoproducao in PedidoProducao.query.all()]

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
            'validade': self.validade.data.strftime('%Y-%m-%d'),
            'status': self.status.data,
            'produto_id': self.produto_id.data,
            'quantidades': self.quantidades.data,
            'produtos': self.produtos.data,

        }

@app.route('/receitas/formulario', methods=['GET', 'POST'])
def exibir_formreceita():
    form = ReceitaForm()
    produtos = Produto.query.all()  # Recupera todos os produtos do banco de dados
  #  produtos_cadastrados = []  # Inicialize a variável para armazenar os produtos cadastrados na receita

    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()

            # Processar os produtos e quantidades selecionados
            produtos_quantidades = {}

            for produto_id, quantidade in zip(form.produtos.data, form.quantidades.data):
                produtos_quantidades[produto_id] = quantidade

            # Cadastrar a receita no banco de dados
            receita_id = receita_service.cadastrar_receita(form_data)

            # Adicionar produtos à receita usando a função adicionar_produto_a_receita
            for produto_id, quantidade in produtos_quantidades.items():
                receita_service.adicionar_produtos_a_receita(receita_id, produto_id, quantidade)

            flash("Receita cadastrada com sucesso!")
            return redirect(url_for("listar_receitas"))

        except ValidationError as error:
            flash("Erro ao cadastrar Receita: " + str(error.messages))

    return render_template('receitas/formreceita.html', form=form, produtos=produtos)

    # Lidar com adição dinâmica de campos
    if 'adicionar_produto' in request.form:
        form.produto_id.choices.append((None, 'Selecione um produto'))
        form.quantidades.choices.append((None, '1'))

    if 'remover_produto' in request.form:
        try:
            index = int(request.form['remover_produto'])
            if index < len(form.produto_id.choices):
                form.produto_id.choices.pop(index)
                form.quantidades.choices.pop(index)
        except ValueError:
            pass

    return render_template('receitas/formreceita.html', form=form,
                           produtos_cadastrados=produtos_cadastrados, produtos=produtos)


@app.route('/receitas/cadastrar_receita', methods=['GET', 'POST'])
def cadastrar_receita_handler():
    try:
        descricao_mix = request.form['descricao_mix']
        modo_preparo = request.form['modo_preparo']
        departamento = request.form['departamento']
        rend_kg = float(request.form['rend_kg'])
        rend_unid = request.form['rend_unid']
        validade = request.form['validade']
        status = request.form['status']
        produto_ids = request.form.getlist('produto_ids[]')
        quantidades = request.form.getlist('quantidades[]')

        # Chame a função de serviço para cadastrar a receita
        sucesso, mensagem = receita_service.cadastrar_receita(
            descricao_mix, modo_preparo, departamento,
            rend_kg, rend_unid, validade, status,
            produto_ids, quantidades)

        if sucesso:
            return redirect(url_for('receitas/formulario_receita', mensagem=mensagem))
        else:
            return render_template('receitas/formulario_receita.html', erro=mensagem)
    except Exception as e:
        return render_template('receitas/formulario_receita.html', erro=str(e))


@app.route('/receitas/adicionar_produtos', methods=['GET', 'POST'])
def adicionar_produtos():
    form = ReceitaForm()  # formulário ReceitaForm para adicionar produtos

    if request.method == 'POST' and form.validate_on_submit():
        # Processar os produtos e quantidades selecionados no novo formulário
        produtos_adicionais = []
        quantidades_adicionais = []

        for i in range(5):  # Ou quantos campos você desejar, deve corresponder ao número definido no template
            produto_id = request.form.get(f"produto_id_{i}")
            quantidade = request.form.get(f"quantidade_{i}")

            # Verificar se o produto_id e quantidade são válidos
            if produto_id and quantidade:
                produtos_adicionais.append(produto_id)
                quantidades_adicionais.append(quantidade)

        # Agora você pode processar e armazenar esses produtos e quantidades no banco de dados ou onde preferir
        receita_service.adicionar_produtos_a_receita(produtos_adicionais, quantidades_adicionais)

    return render_template('receitas/adicionar_produtos.html', form=form)


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

           # produtos_quantidades = receita_service.obter_produtos_da_receita(receita_data['id'])
          #  receita_data['produtos_quantidades'] = produtos_quantidades

            return render_template('receitas/detalhes.html', receita=receita_data)
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
