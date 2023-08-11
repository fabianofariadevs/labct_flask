from flask import request, render_template, redirect, url_for, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from api import app, api, db
from ..models import filial_pdv_model
from ..services import filial_pdv_service
from ..schemas import filial_pdv_schema
from ..schemas.filial_pdv_schema import FilialSchema
from ..models.cliente_model import Cliente
from ..paginate import paginate

#TODO ** Classe FilialForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria

class FilialForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    responsavel = StringField('Responsável', validators=[DataRequired()])
    whatsapp = StringField('WhatsApp', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])
  #  receitas = SelectField('Receitas', validators=[DataRequired()])
    cliente = SelectField('Vincular Fábrica', validators=[DataRequired()])
    #pedidos = SelectField('Pedidos_Compras', validators=[DataRequired()])
    #pedidosprod = SelectField('Pedidos_Compras', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(FilialForm, self).__init__(*args, **kwargs)
      #  self.receitas.choices = [(receita.id, receita.descricao_mix) for receita in Receita.query.all()]
        self.cliente.choices = [(cliente.id, cliente.nome) for cliente in Cliente.query.all()]
       # self.pedidos.choices = [(produto.id, produto.nome) for produto in Produto.query.all()]
       # self.pedidosprod.choices = [(pedidoproducao.id, pedidoproducao.receita_id) for pedidoproducao in PedidoProducao.query.all()]
        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    def to_dict(self):  # metodo personalizado no seu formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
        return {
            'nome': self.nome.data,
            'endereco': self.endereco.data,
            'bairro': self.bairro.data,
            'cidade': self.cidade.data,
            'estado': self.estado.data,
            'responsavel': self.responsavel.data,
            'whatsapp': self.whatsapp.data,
            'cnpj': self.cnpj.data,
            'status': self.status.data,
            'cliente': self.cliente.data,
          #  'receitas': self.receitas.data,
         #   'pedidos': self.pedidos.data,
           # 'pedidosprod': self.pedidosprod.data,
        }

@app.route('/filiais/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_filial(id):
    filial = filial_pdv_service.listar_filial_pdv_id(id)
    if not filial:
        return render_template("filiais/filial.html", error_message="Filial não encontrada"), 404
    form = FilialForm(obj=filial)
    if form.validate_on_submit():
        filial_atualizada = filial_pdv_model.Filial.query.get(id)
        form.populate_obj(filial_atualizada)
        filial_pdv_service.atualiza_filial_pdv(filial, filial_atualizada)
        return redirect(url_for("listar_filiais"))

    return render_template('filiais/formfilial.html', filial=filial, form=form), 400


@app.route('/filiais', methods=['GET'])###1
def listar_filiais():
    if request.method == 'GET':
        filiais = filial_pdv_service.listar_filial_pdv()
        filiais_data = filial_pdv_schema.FilialSchema().dump(filiais, many=True)
        #filiais_data = [filial_pdv_schema.FilialSchema().add_links(filial_data) for filial_data in filiais_data]
        total_filiais = len(filiais)
        total_filiais_ativos = len([filial for filial in filiais if filial.status == 1])
        total_filiais_inativos = len([filial for filial in filiais if filial.status == 0])

        return render_template('filiais/filial.html', filiais=filiais_data, total_filiais=total_filiais,
                               total_filiais_ativos=total_filiais_ativos,
                               total_filiais_inativos=total_filiais_inativos)


@app.route('/filiais/formulario', methods=['GET', 'POST'])###2
def exibir_formfilial():
    form = FilialForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            filial = filial_pdv_schema.FilialSchema().load(form_data)
            filial_bd = filial_pdv_service.cadastrar_filial_pdv(filial)
            filial_data = filial_pdv_schema.FilialSchema().dump(filial_bd)
            flash("Filial cadastrada com sucesso!")
            return redirect(url_for('listar_filiais'))
        except ValidationError as error:
            flash("Erro ao cadastrar filial: " + str(error.messages))
    return render_template('filiais/formfilial.html', form=form)###3


@app.route('/filiais/<int:id>', methods=['GET', 'PUT'])
def visualizar_filial(id):
    filial = filial_pdv_service.listar_filial_pdv_id(id)
    return render_template('filiais/detalhes.html', filial=filial)


@app.route('/filiais99/<int:id>', methods=['GET', 'PUT'])
def visualizar_filial99(id):
###if request.method == 'GET':
#    filial = filial_pdv_service.listar_filial_pdv_id(id)
    if filial:
        filial_data = filial_pdv_schema.FilialSchema().dump(filial)

        # Obter o nome do receita
        receitas = filial.receitas
        filial_data['receitas'] = filial.receitas.nome if receitas else 'Receita não encontrado'

        # Obter o nome do pedido de Compras
        pedido = filial.pedidos
        filial_data['pedidos'] = pedido.produto.nome if pedido else 'Produto não encontrado'

        # Obter o nome do Cliente
        cliente = filial.clientes
        filial_data['clientes'] = cliente.nome if cliente else 'Filial não encontrada'

        # Obter o nome do PEDIDO DE PRODUÇAO
        pedidoproducao = filial.pedidosprod
        filial_data['pedidosprod'] = pedidoproducao.receita_id if pedidoproducao else 'Filial não encontrada'

        return render_template('filiais/detalhes.html', filial=filial_data)
    else:
        # Caso o pedido não seja encontrado, retorne uma mensagem de erro
        return render_template('error.html', message='Pedido não encontrado', status_code=404)


@app.route('/filiais/<int:id>/deletar', methods=['DELETE'])
def deletar_filial(id):
    filial = filial_pdv_service.listar_filial_pdv_id(id)
    if filial:
        filial_pdv_service.remove_filial_pdv(filial)
        return redirect(url_for('listar_filiais'))
    else:
        return render_template('filiais/formfilial.html', message='Filial não encontrada'), 404



