from flask import Flask, render_template, request, redirect, make_response, url_for, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
#from flask_jwt_extended import JWTManager
from flask_wtf import FlaskForm
import json

#from .views.cliente_views import ClienteForm


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


@app.route('/historico')
def historicocompras():
    return render_template('estoque/historicocompras.html')

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




from .views import usuario_views, cliente_views, login_views, filial_pdv_views, receita_views, fornecedor_views, produtoMp_views, mix_produto_views, pedido_views
from .models import usuario_model, cliente_model, filial_pdv_model, receita_model, fornecedor_model, produtoMp_model, mix_produto_model, pedido_model

