from sqlalchemy.orm import joinedload
from api import app, api, db
from ..schemas import usuario_schema
from flask import request, make_response, jsonify, render_template, url_for, redirect, flash
from ..services import usuario_service
from ..models.cliente_model import Cliente
from ..models.usuario_model import Funcao, Usuario
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError

class UsuarioForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    senha = StringField('Senha', validators=[DataRequired()])
    is_admin = SelectField('Administrador', choices=[("1", 'Sim'), ("0", 'Não')], validators=[DataRequired()], coerce=int)
    status = SelectField('Status', choices=[("1", 'Ativo'), ("0", 'Inativo')], validators=[DataRequired()], coerce=int)
    cliente = SelectField('Empresa/Cliente', validators=[DataRequired()], coerce=int)
    funcao = SelectField('Função', validators=[DataRequired()], coerce=int)

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.cliente.choices = [(cliente.id, cliente.nome)
                                for cliente in Cliente.query.all()]
        self.funcao.choices = [(funcao.id, funcao.nome)
                               for funcao in Funcao.query.all()]

        self.is_admin.choices = self.get_is_admin_choices()
        self.status.choices = self.get_status_choices()

    @staticmethod
    def get_is_admin_choices():
        return [("1", 'Sim'), ("0", 'Não')]

    @staticmethod
    def get_status_choices():
        return [("1", 'Ativo'), ("0", 'Inativo')]

    def to_dict(self):
        data = {
            "nome": self.nome.data,
            "email": self.email.data,
            "senha": self.senha.data,
            "is_admin": self.is_admin.data,
            "status": self.status.data,
            "cliente": int(self.cliente.data) if self.cliente.data else None,
            "funcao": int(self.funcao.data) if self.funcao.data else None,
        }
        return data


@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    if request.method == 'GET':
        usuarios = Usuario.query.options(joinedload("cliente")).options(joinedload("funcao")).all()
        usuarios_data = []
        for usuario in usuarios:
            usuario_dict = usuario_schema.UsuarioSchema().dump(usuario)

            cliente = usuario.cliente
            usuario_dict['cliente'] = cliente.nome if cliente else None

            funcao = usuario.funcao
            usuario_dict['funcao'] = funcao.nome if funcao else None

            usuarios_data.append(usuario_dict)

        total_usuarios = len(usuarios)
        total_usuarios_ativos = len([usuario for usuario in usuarios if usuario.status == 1])
        total_usuarios_inativos = len([usuario for usuario in usuarios if usuario.status == 0])

        return render_template("usuarios/usuarios.html", usuarios=usuarios_data, total_usuarios=total_usuarios,
                               total_usuarios_ativos=total_usuarios_ativos,
                               total_usuarios_inativos=total_usuarios_inativos)


@app.route('/usuarios/<int:id>/atualizar', methods=['GET', 'POST', 'PUT'])
def atualizar_usuario(id):
    usuario = usuario_service.listar_usuario_id(id)
    if not usuario:
        return render_template("usuarios/usuarios.html", error_message="Usuario não encontrado"), 404

    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario_atualizado = Usuario.query.get(id)
        form.populate_obj(usuario_atualizado)
        usuario_service.atualizar_usuario(usuario, usuario_atualizado)
        return redirect(url_for("listar_usuarios"))

    return render_template("usuarios/formusuario.html", usuario=usuario, form=form), 400

@app.route('/usuarios/formulario', methods=['GET', 'POST'])
def exibir_formusuario():
    form = UsuarioForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form_data = form.to_dict()
            usuario = usuario_schema.UsuarioSchema().load(form_data)
           # form.populate_obj(usuario)
            usuario_bd = usuario_service.cadastrar_usuario(usuario)
            usuario_data = usuario_schema.UsuarioSchema().dump(usuario_bd)
            flash("Usuário cadastrado com sucesso!")
            return redirect(url_for("listar_usuarios"))
        except ValidationError as error:
            flash("Erro ao cadastrar Usuário")
    return render_template('usuarios/formusuario.html', form=form, usuario={})

@app.route('/usuarios/buscar', methods=['GET'])
def buscar_usuario():
    nome_usuario = request.args.get('nome_usuario', '').strip().lower()
    resultados = None

    if nome_usuario:
        # Lógica para buscar o usuario por nome
        usuarios = usuario_service.listar_usuarios()
        resultados = [usuario for usuario in usuarios if nome_usuario in usuario.nome.lower()]

    return render_template("usuarios/consultar_usuario.html", resultados=resultados, nome_usuario=nome_usuario)

@app.route('/usuarios/<int:id>', methods=['GET', 'POST'])
def visualizar_usuario(id):
    #usuario = usuario_service.listar_usuario_id(id)
    #return render_template('usuarios/detalhes.html', usuario=usuario)
    if request.method == 'GET':
        usuario = usuario_service.listar_usuario_id(id)
        if usuario:
            usuario_data = usuario_schema.UsuarioSchema().dump(usuario)

            # Obter o nome da Empresa Contratante
            cliente = usuario.cliente
            usuario_data['empresa'] = cliente.nome if cliente else 'Empresa não encontrada'

            funcao = usuario.funcao
            usuario_data['cargo'] = funcao.nome if funcao else 'Função não encontrada'

            return render_template('usuarios/detalhes.html', usuario=usuario_data)
        else:
            # Caso o usuario não seja encontrado, retorne uma mensagem de erro
            return render_template('error.html', message='Usuário não encontrado', status_code=404)

    elif request.method == 'POST':  # método DELETE
        if request.form.get('_method') == 'DELETE':
            usuario = usuario_service.listar_usuario_id(id)
            if usuario:
                usuario_service.deletar_usuario(usuario)
                return redirect(url_for('listar_usuarios'))


@app.route('/usuarios/<int:id>/deletar', methods=['DELETE'])
def deletar_usuario(id):
    usuario = usuario_service.listar_usuario_id(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    return redirect(url_for('listar_usuarios'))