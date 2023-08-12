from flask_restful import Resource
from ..schemas import operacao_schema
from flask import request, make_response, jsonify
from ..entidades import operacao
from ..services import operacao_service, estoque_service
from api import api

class OperacaoList(Resource):

    def get(self):
        operacoes = operacao_service.listar_operacoes()
        os = operacao_schema.OperacaoSchema(many=True)
        return make_response(os.jsonify(operacoes), 201)

    def post(self):
        os = operacao_schema.OperacaoSchema()
        validate = os.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            cliente_id = request.json["cliente_id"]
            produto_id = request.json["produto_id"]
            qtde = request.json["qtde"]
            tipo = request.json["tipo"]
            estoque_id = request.json["estoque_id"]
            if estoque_service.listar_estoque_id(estoque_id) is None:
                return make_response("Estoque não existe", 404)
            else:
                operacao_nova = operacao.Operacao(
                    cliente_id=cliente_id,
                    produto_id=produto_id,
                    qtde=qtde,
                    tipo=tipo,
                    estoque_id=estoque_id
                )
            resultado = operacao_service.cadastrar_operacao(operacao_nova)
            return make_response(os.jsonify(resultado),201)

class OperacaoDetail(Resource):

    def get(self, id):
        operacao = operacao_service.listar_operacao_id(id)
        if operacao is None:
            return make_response(jsonify("Operação Não Encontrada"), 404)
        os = operacao_schema.OperacaoSchema()
        return make_response(os.jsonify(operacao), 200)

    def put(self, id):
        operacao_bd = operacao_service.listar_operacao_id(id)
        if operacao_bd is None:
            return make_response(jsonify("Operação Não Encontrada"), 404)
        os = operacao_schema.OperacaoSchema()
        validate = os.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            cliente_id = request.json["cliente_id"]
            produto_id = request.json["produto_id"]
            qtde = request.json["qtde"]
            tipo = request.json["tipo"]
            estoque_id = request.json["estoque_id"]
            print(estoque_id)
            if estoque_service.listar_estoque_id(estoque_id) is None:
                return make_response("Estoque não existe", 404)
            else:
                operacao_nova = operacao.Operacao(
                    cliente_id=cliente_id,
                    produto_id=produto_id,
                    qtde=qtde,
                    tipo=tipo,
                    estoque_id=estoque_id
                )
            resultado = operacao_service.atualizar_operacao(operacao_bd, operacao_nova)
            return make_response(os.jsonify(resultado), 201)

    def delete(self, id):
        operacao = operacao_service.listar_operacao_id(id)
        if operacao is None:
            return make_response(jsonify("Operação Não Encontrada"), 404)
        operacao_service.exclui_operacao(operacao)
        return make_response(jsonify(""), 204)


api.add_resource(OperacaoList, '/operacoes')
api.add_resource(OperacaoDetail, '/operacoes/<int:id>')