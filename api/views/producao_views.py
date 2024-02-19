from api import app, db
from flask import render_template, request, redirect, url_for, flash
from ..models.filial_pdv_model import Filial
from ..models.mix_produto_model import MixProduto
from ..models.producao_model import Producao
from ..models.pedido_model import PedidoProducao
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError

class ProducaoForm(FlaskForm):
    data_producao = StringField('Nome', validators=[DataRequired()])
    qtde_produzida = StringField('Descrição', validators=[DataRequired()])
    qrcode = StringField('Qrcode')
    obs = StringField('Obs')
    status = SelectField('Status', choices=[("0", 'Aberto'), ("1", 'em Produção'), ("2", 'Liberado para entrega'), ("3", 'Entregue'), ("4", 'Cancelado')], default=0, validators=[DataRequired()])
    mixprodutos = SelectField('MixProduto', validators=[DataRequired()], coerce=int)
    filial = SelectField('Filial', validators=[DataRequired()], coerce=int)
    pedidosprod = SelectField('Pedido Produção', validators=[DataRequired()], coerce=int)

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(ProducaoForm, self).__init__(*args, **kwargs)

        self.mixprodutos.choices = [(mixproduto.id, mixproduto.nome)
                                    for mixproduto in MixProduto.query.all()]

        self.filial.choices = [(filial.id, filial.nome)
                               for filial in Filial.query.all()]

        self.pedidosprod.choices = [(pedidoproducao.id, pedidoproducao.receita_id)
                                    for pedidoproducao in PedidoProducao.query.all()]

        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("0", 'Aberto'), ("1", 'em Produção'), ("2", 'Liberado para entrega'), ("3", 'Entregue'), ("4", 'Cancelado')]

    def to_dict(self):  # metodo personalizado no seu formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
        return {
            'mixprodutos': self.mixprodutos.data,
            'filial': self.filial.data,
            'data_producao': self.data_producao.data,
            'qtde_produzida': self.qtde_produzida.data,
            'qrcode': self.qrcode.data,
            'obs': self.obs.data,
            'status': self.status.data,
            'pedidosprod': self.pedidosprod.data,
        }

@app.route('/producao/lista', methods=['GET'])
def listar_producao():
    producoes = Producao.query.all()
    return render_template('producao/lista.html', producoes=producoes)

@app.route('/producao/buscar', methods=['GET'])
def buscar_producao():
    nome_mixproduto = request.args.get('nome_mixproduto', '').strip().lower()

    if nome_mixproduto:
        produtosmix = Producao.query.filter(Producao.mixprodutos.ilike(f'%{nome_mixproduto}%')).all()
    else:
        produtosmix = Producao.query.all()

    return render_template('producao/lista.html', produtosmix=produtosmix)

@app.route('/solicitacoes/lista', methods=['GET'])
def listar_solicitacoes():
    solicitacoes = PedidoProducao.query.all()
    return render_template('producao/solicitacoes.html', solicitacoes=solicitacoes)

@app.route('/producao/cadastrar', methods=['GET', 'POST'])
def cadastrar_producao():
    form = ProducaoForm()

    if form.validate_on_submit():
        producao = Producao(**form.to_dict())
        db.session.add(producao)
        db.session.commit()

        return redirect(url_for('listar_producao'))

    return render_template('producao/form.html', form=form)

@app.route('/producao/<int:id>', methods=['GET', 'POST'])
def visualizar_producao(id):
    producao = Producao.query.get(id)
    form = ProducaoForm(obj=producao)

    if form.validate_on_submit():
        form_data = form.to_dict()
        producao.mixproduto_id = form_data['mixproduto_id']
        producao.filial_id = form_data['filial_id']
        producao.data_producao = form_data['data_producao']
        producao.qtde_produzida = form_data['qtde_produzida']
        producao.qrcode = form_data['qrcode']
        producao.status = form_data['status']
        producao.pedidosprod_id = form_data['pedidosprod_id']

        db.session.commit()

        return redirect(url_for('listar_producao'))

    return render_template('producao/form.html', form=form)

@app.route('/producao/<int:id>/excluir', methods=['GET', 'POST'])
def excluir_producao(id):
    producao = Producao.query.get(id)

    if producao:
        db.session.delete(producao)
        db.session.commit()

    return redirect(url_for('listar_producao'))

# TODO: Atualizar status da produção e estoque.
@app.route('/producao/atualizar/<int:id>', methods=['POST'])
def atualizar_producao(id):
    producao = Producao.query.get(id)

    if producao and str(producao.status) == '0':
        # Atualize o status da produção para 'em Aberto'.
        producao.status = 'Aberto'
        db.session.commit()

        flash("Produção atualizada com sucesso!")

    elif producao and str(producao.status) == '1':
        # Atualize o status da produção para 'em Produção'.
        producao.status = 'em Produção'
        db.session.commit()

        flash("Produção atualizada com sucesso!")

    elif producao and str(producao.status) == '2':
        # Atualize o status da produção para 'Liberado para entrega'.
        producao.status = 'Liberado para entrega'
        db.session.commit()

        # Atualize o estoque com base na quantidade produzida e entregue.
        mixproduto = producao.mixproduto
        mixproduto.situacao = 'Liberado para entrega'
        mixproduto.qtde_produzida += producao.qtde_produzida
        db.session.commit()

        flash("Produção atualizada com sucesso!")

    elif producao and str(producao.status) == '3':
        producao.status = 'Entregue'
        db.session.commit()

        # Atualize o estoque com base na quantidade produzida e entregue.
        mixproduto = producao.mixproduto
        mixproduto.situacao = 'Entregue'
        mixproduto.qtde_entregue += producao.qtde_produzida
        db.session.commit()

        flash("Produção atualizada com sucesso!")

    elif producao and str(producao.status) == '4':
        producao.status = 'Cancelado'
        db.session.commit()

        # Atualize o estoque com base na quantidade produzida e entregue.
        mixproduto = producao.mixproduto
        mixproduto.situacao = 'Cancelado'
        mixproduto.qtde_produzida -= producao.qtde_produzida
        db.session.commit()

        flash("Produção atualizada com sucesso!")
    else:
        flash("Erro ao atualizar produção!")

    return redirect(url_for('listar_producao'))

#TODO View para atualizar o estoque e situação do Mix Produto para 'Liberado para entrega'.
@app.route('/producao/entregar/<int:id>', methods=['POST'])
def entregar_producao(id):
    producao = Producao.query.get(id)

    if producao and str(producao.status) == '2':
        # Atualize o status da produção para 'Liberado para entrega'.
        producao.status = 'Liberado para entrega'
        db.session.commit()

        # Atualize o estoque com base na quantidade produzida e entregue.
        mixproduto = producao.mixproduto
        mixproduto.situacao = 'Liberado para entrega'
        mixproduto.qtde_produzida += producao.qtde_produzida
        db.session.commit()

        flash("Produção atualizada com sucesso!")
    else:
        flash("Erro ao atualizar produção!")

    return redirect(url_for('listar_producao'))
