from api import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField, FloatField, FieldList, FormField, Form, IntegerField
from wtforms.fields import SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, length
from ..schemas import receita_schema
from flask import request, make_response, jsonify, render_template, redirect, url_for, flash, session
from ..services import receita_service
from ..models.receita_model import Receita
from ..paginate import paginate
from ..models.produtoMp_model import Produto, receita_produto
from ..models.filial_pdv_model import Filial
from sqlalchemy.orm import joinedload

class ProdutoReceitaForm(FlaskForm):
    produto_id = SelectField('Produto', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', default=1, validators=[DataRequired()])
    #produtos = SelectMultipleField('Produtos', validators=[DataRequired()])

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(ProdutoReceitaForm, self).__init__(*args, **kwargs)
        self.produto_id.choices = [(produto.id, produto.nome)
                                   for produto in Produto.query.all()]

        #self.produtos.choices = [(produto.id, produto.nome) for produto in Produto.query.all()]

        # Adicionar opções para quantidades, por exemplo, de 1 a 10
        self.quantidade.choices = [(i, str(i)) for i in range(1, 21)]  # Altere o intervalo conforme necessário

    def to_dict(self):
        return {
            'produto_id': self.produto_id.data,
            'quantidade': self.quantidade.data,
        }

class ReceitaForm(FlaskForm):
    descricao_mix = StringField("Descricao_mix", validators=[DataRequired()])
    modo_preparo = StringField("Modo_preparo", validators=[DataRequired()])
    departamento = StringField('Departamento', validators=[DataRequired()])
    rend_kg = FloatField('Rend_kg', validators=[DataRequired()])
    rend_unid = FloatField('Rend_unid', validators=[DataRequired()])
    validade = DateField('Validade', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
#    atualizado_em = DateField('atualizado_em', format='%d/%m/%Y')
    #produto_id = SelectField('Produto', choices=[('1', 'Produto 1'), ('2', 'Produto 2')])

    produto_id = SelectMultipleField('Produtos', coerce=int)
    quantidade = SelectMultipleField('Quantidades', default=1, validators=[DataRequired()])
    produtos = SelectMultipleField('Produtos')
    filial = StringField('Filial Relacionada')
   # pedidoprod = StringField('Pedido de Produção', validators=[DataRequired()])
    #produtos = [(1, 'Produto 1'), (2, 'Produto 2')]  # Exemplo de produtos

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        self.produto_id.choices = [(produto.id, produto.nome)
                                   for produto in Produto.query.all()]

        self.produtos.choices = [(produto.id, produto.nome)
                                 for produto in Produto.query.all()]

        self.filial.choices = [(filial.id, filial.nome)
                               for filial in Filial.query.all()]

        # Adicionar opções para quantidades, por exemplo, de 1 a 10
        self.quantidade.choices = [(i, str(i)) for i in range(1, 21)]  # Altere o intervalo conforme necessário
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
            'quantidade': self.quantidade.data,
            'produtos': self.produtos.data,
            'filial': self.filial.data,

        }

@app.route('/receitas/formulario', methods=['GET', 'POST'])
def exibir_formreceita():
    form = ReceitaForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()

            # Processar os produtos e quantidades selecionados
            produtos_ids = form.produto_id.data
            quantidades = form.quantidade.data

            # Verificar se produtos_ids e quantidades são listas ou sequências
            if not isinstance(produtos_ids, (list, tuple)):
                produtos_ids = [produtos_ids]

            if not isinstance(quantidades, (list, tuple)):
                quantidades = [quantidades]
            # Certifique-se de que ambos os campos têm a mesma quantidade de itens
            if len(produtos_ids) != len(quantidades):
                raise ValueError("Número de produtos e quantidades não correspondem.")

            # Mapeie os produtos e quantidades em um dicionário
            produtos_quantidades = {int(produto_id): int(quantidade) for produto_id, quantidade in
                                    zip(produtos_ids, quantidades)}

            nova_receita = receita_service.cadastrar_receita(form_data, produtos_quantidades)

            # Adicionar produtos à receita usando a função adicionar_produtos_a_receita
            receita_service.adicionar_produtos_e_quantidades_a_receita(nova_receita.id, produtos_quantidades) # ou produtos_ids, quantidades

            flash("Receita cadastrada com sucesso!")

            return redirect(url_for('visualizar_receita', id=nova_receita.id))
           # return redirect(url_for("listar_receitas"))

        except ValidationError as error:
            flash("Erro ao cadastrar Receita: " + str(error.messages))

    produtos = Produto.query.all()
    return render_template('receitas/formreceita.html', form=form, produtos=produtos, receita_produto=session.get('receita_produto', []))


@app.route('/receitas/adicionar_produto', methods=['POST'])
def adicionar_produto():
    form = ProdutoReceitaForm(request.form)
    #produtos_da_receita = []

    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Processar os dados do formulário
            produto_id = form.produto_id.data
            quantidade = form.quantidade.data

            # Inicializa a lista de produtos da receita na sessão se ainda não existir
            if 'receita_produto' not in session:
                session['receita_produto'] = []

            # Verifique se o produto já está na lista de produtos da receita
            for produto in session['receita_produto']:
                if produto['id'] == produto_id:
                    produto['quantidade'] += quantidade
                    break
            else:
                # Se o produto não estiver na lista, adicione-o
                session['receita_produto'].append({
                    'id': produto_id,
                    'quantidade': quantidade,
                })

            return redirect(url_for("listar_receitas"))

        except ValidationError as error:
            flash("Erro ao adicionar produto: " + str(error.messages))

    return render_template('receitas/adicionar_produtos.html', form=form, receita_produto=session.get('receita_produto', []))

# Rota para listar os produtos da receita
@app.route('/receitas/listar_produtos', methods=['GET'])
def listar_produtosreceita():
    produtos_da_receita = session.get('produtos_da_receita', [])
    return render_template('receitas/listar_produtos.html', produtos_da_receita=produtos_da_receita)


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
