from api import app, api, db
from ..schemas import usuario_schema
from flask import request, make_response, jsonify, render_template, url_for, redirect
from ..models import usuario_model
from ..entidades import usuario
from ..services import usuario_service
from ..models.cliente_model import Cliente
from ..models.usuario_model import Funcao, Usuario
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
import uuid

class UsuarioForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    senha = StringField('senha', validators=[DataRequired()])
    is_admin = BooleanField('is_admin', validators=[DataRequired()])
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()])

    empresa = SelectField('Empresa/Cliente', validators=[DataRequired()])
    cargo = SelectField('Função', validators=[DataRequired()])

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.empresa.choices = [(cliente.id, cliente.nome)
                                for cliente in Cliente.query.all()]

        self.cargo.choices = [(funcao.id, funcao.nome)
                              for funcao in Funcao.query.all()]
        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    #TODO metodo personalizado no seu formulário para extrair os dados do formulário em um formato serializável, como um dicionário.
    def to_dict(self):
        return {
            'nome': self.nome.data,
            'email': self.email.data,
            'senha': self.senha.data,
            'is_admin': self.is_admin.data,
            'status': self.status.data,
            'empresa': self.empresa.data,
            'cargo': self.cargo.data,
        }
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    if request.method == 'GET':
        usuarios = usuario_service.listar_usuarios()
        usuarios_data = usuario_schema.UsuarioSchema().dump(usuarios, many=True)
        total_usuarios = len(usuarios)
        total_usuarios_ativos = len([produto for produto in usuarios if produto.status == True])
        total_usuarios_inativos = len([produto for produto in usuarios if produto.status == False])

        return render_template("usuarios/usuarios.html", usuarios=usuarios_data, total_usuarios=total_usuarios,
                               total_usuarios_ativos=total_usuarios_ativos,
                               total_usuarios_inativos=total_usuarios_inativos)


@app.route('/usuarios/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_usuario(id):
    usuario = usuario_service.listar_usuario_id(id)
    if not usuario:
        #return "Cliente não encontrado", 404
        return render_template("usuarios/usuarios.html", error_message="Usuario não encontrado"), 404
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario_atualizado = Usuario.query.get(id)
        form.populate_obj(usuario_atualizado)
        usuario_service.atualizar_usuario(usuario, usuario_atualizado)
        return redirect(url_for("listar_usuarios"))

    return render_template("usuarios/formusuario.html", usuario=usuario, form=form), 400


@app.route('/usuarios/formulario', methods=['GET', 'POST', 'PUT'])
def exibir_formusuario():
    form = UsuarioForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            usuario = usuario_schema.UsuarioSchema().load(form_data)
            usuario_bd = usuario_service.cadastrar_usuario(usuario)
            usuario_data = usuario_schema.UsuarioSchema().dump(usuario_bd)
            return redirect(url_for("usuarios/listar_usuarios", form=form, form_data=form_data, usuario=usuario_bd))
        except ValidationError as error:
            return render_template('usuarios/formusuario.html', form=form, error_message=error.messages)
    else:
        return render_template('usuarios/formusuario.html', form=form, error_message=form.errors)


@app.route('/usuarios/<int:id>', methods=['GET', 'PUT'])
def visualizar_usuario(id):
    usuario = usuario_service.listar_usuario_id(id)
    return render_template('usuarios/detalhes.html', usuario=usuario)


@app.route('/usuarios/<int:id>/deletar', methods=['DELETE'])
def deletar_usuario(id):
    usuario = usuario_service.listar_usuario_id(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    return redirect(url_for('listar_usuarios'))