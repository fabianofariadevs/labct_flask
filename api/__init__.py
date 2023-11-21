from flask import Flask, render_template, request, redirect, make_response, url_for, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FloatField, DateField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
import json

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)
# jwt = JWTManager

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/painelestoque')
def listar_painel():
    return render_template('estoque/estoque.html')


@app.route('/invenario')
def inventario():
    return render_template('estoque/inventario.html')

@app.route('/producao')
def producao():
    return render_template('producao.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contatos')
def contatos():
    return render_template('contato.html')

@app.route('/clubeterra')
def clubeterra():
    return render_template('clubeterra.html')


from .views import usuario_views, cliente_views, login_views, filial_pdv_views, receita_views, fornecedor_views, produtoMp_views, mix_produto_views, pedido_views, estoque_views, producao_views
from .models import usuario_model, cliente_model, filial_pdv_model, receita_model, fornecedor_model, produtoMp_model, mix_produto_model, pedido_model, estoque_model
