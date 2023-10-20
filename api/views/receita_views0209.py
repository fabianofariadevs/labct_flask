from api import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField, FloatField, FieldList, FormField
from wtforms.fields import SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from ..schemas import receita_schema
from flask import request, make_response, jsonify, render_template, redirect, url_for, flash
from ..services import receita_service
from ..models.receita_model import Receita
from ..paginate import paginate
from ..models.produtoMp_model import Produto
from ..models.filial_pdv_model import Filial
from sqlalchemy.orm import joinedload

class ReceitaProdutoForm(FlaskForm):
    produto_id = SelectField('Produtos', validators=[DataRequired()])
    quantidade = SelectField('Quantidades', coerce=int, validators=[DataRequired()])

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
    quantidades = SelectMultipleField('Quantidades', coerce=int, validators=[DataRequired()])
    #filial = StringField('Filial Relacionada', validators=[DataRequired()])
   # pedidoprod = StringField('Pedido de Produção', validators=[DataRequired()])
    #produtos = [(1, 'Produto 1'), (2, 'Produto 2')]  # Exemplo de produtos

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        self.produto_id.choices = [(produto.id, produto.nome)
                                   for produto in Produto.query.all()]
        # Adicionar opções para quantidades, por exemplo, de 1 a 10
        self.quantidades.choices = [(i, str(i)) for i in range(1, 11)]  # Altere o intervalo conforme necessário
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
        }

@app.route('/receitas/formulario', methods=['GET', 'POST'])
def exibir_formreceita():
    form = ReceitaForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            # processar os produtos selecionados corretamente, é uma lista de IDs de produtos.
            produtos_selecionados = form_data.pop('produto_id', [])
            quantidades_selecionadas = request.form.getlist('quantidade')  # campos de quantidade
            receita = receita_schema.ReceitaSchema().load(form_data)
            receita_bd = receita_service.cadastrar_receita(receita)
            receita_data = receita_schema.ReceitaSchema().dump(receita_bd)
            # Criar a Receita e associar os produtos selecionados
            receita = receita_service.cadastrar_receita(form_data)
            for produto_id, quantidade in zip(produtos_selecionados, quantidades_selecionadas):
                # Crie uma associação entre a Receita e o Produto com a quantidade
                receita_service.adicionar_produtos_e_quantidades_a_receita(receita, produto_id, quantidade)

            flash("Receita cadastrada com sucesso!")
            return redirect(url_for("listar_receitas"))
        except ValidationError as error:
            flash("Erro ao cadastrar Receita")
    return render_template('receitas/formreceita.html', form=form)


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
        #return "Cliente não encontrado", 404
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
