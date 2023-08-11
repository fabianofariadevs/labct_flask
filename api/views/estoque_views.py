from ..schemas import estoque_schema
from flask import request, render_template, jsonify
from ..entidades import estoque
from ..services import estoque_service
from api import app
from flask_jwt_extended import jwt_required

#TODO ** Classe EstoqueForm_Modelo ** ESSA classe recebe os dados do formulario.
#     @author Fabiano Faria

@app.route('/estoques', methods=['GET'])###1
def listar_pal():
    if request.method == 'GET':
        le = estoque_service.listar_estoque()
        listas = estoque_schema.EstoqueSchema().dump(le, many=True)
        return render_template('estoque/estoque.html', le=le, listas=listas)




