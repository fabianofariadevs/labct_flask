from api import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from ..schemas import receita_schema
from flask import request, make_response, jsonify, render_template, redirect, url_for, flash
from ..services import receita_service
from ..models import receita_model
from ..paginate import paginate
from ..models.produtoMp_model import Produto
from ..models.filial_pdv_model import Filial
from ..models.pedido_model import PedidoProducao


class ReceitaForm(FlaskForm):
    descricao_mix = StringField("descricao_mix", validators=[DataRequired()])
    modo_preparo = StringField("modo_preparo", validators=[DataRequired()])
    departamento = StringField('departamento', validators=[DataRequired()])
    rend_kg = StringField('rend_kg', validators=[DataRequired()])
    rend_unid = StringField('rend_unid', validators=[DataRequired()])
    validade = DateField('validade', format='%d/%m/%Y', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
    cadastrado_em = DateField('cadastrado_em', format='%d/%m/%Y')
    atualizado_em = DateField('atualizado_em', format='%d/%m/%Y')
    produto_id = StringField('produtos', validators=[DataRequired()])
    filial = StringField('Filial Relacionada', validators=[DataRequired()])
    pedidoprod = StringField('Pedido de Produção', validators=[DataRequired()])

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        self.produto_id.choices = [(produto.id, produto.nome)
                                   for produto in Produto.query.all()]
        self.filial.choices = [(filial.id, filial.nome)
                               for filial in Filial.query.all()]
        self.pedidoprod.choices = [(pedidoproducao.id, pedidoproducao.receitas)
                               for pedidoproducao in PedidoProducao.query.all()]

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
            'validade': self.validade.data,
            'status': self.status.data,
            'cadastrado_em': self.cadastrado_em.data,
            'atualizado_em': self.atualizado_em.data,
            'produto_id': self.produto_id.data,
            'filial': self.filial.data,
            'pedidoprod': self.pedidoprod.data,
        }


@app.route('/receitas/formulario', methods=['GET', 'POST'])
def exibir_formreceita():
    form = ReceitaForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            receitaform = receita_schema.ReceitaSchema().load(form_data)
            receita_bd = receita_service.cadastrar_receita(receitaform)
            receita_data = receita_schema.ReceitaSchema().dump(receita_bd)
            flash("Receita cadastrada com sucesso!")
            # Redirecionar para a página de listagem de Receitas após o cadastro bem-sucedido
            return redirect(url_for("listar_receitas"))
        except ValidationError as error:
            flash("Erro ao cadastrar Receita")
    return render_template('receitas/formreceita.html', form=form)


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
        return render_template("receitas/receita.html", error_message="Receita não encontrado"), 404

    form = ReceitaForm(obj=atuareceita)
    if request.method == 'POST' and form.validate_on_submit():
        receita_atualizado = receita_model.Receita.query.get(id)
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
            produto = receita.produtos
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
            return render_template('error.html', message='receita não encontrada', status_code=404)

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
