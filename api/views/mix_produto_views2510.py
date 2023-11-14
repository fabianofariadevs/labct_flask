from flask_restful import Resource
from api import api
from ..schemas import mix_produto_schema
from flask import request, make_response, jsonify
from ..entidades import mix_produto
from ..services import mix_produto_service
from ..paginate import paginate
from ..models.mix_produto_model import Mixproduto

class MixprodutoList(Resource):
    def get(self):
        ms = mix_produto_schema.MixprodutoSchema(many=True)
        return paginate(Mixproduto, ms)

    def post(self):
        ms = mix_produto_schema.MixprodutoSchema()
        validate = ms.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            cliente = request.json["cliente"]
            cod_prod_mix = request.json["cod_prod_mix"]
            produto = request.json["produto"]
            descricao = request.json["descricao"]
            modo_preparo = request.json["modo_preparo"]
            departamento = request.json["departamento"]
            rend_kg = request.json["rend_kg"]
            rend_unid = request.json["rend_unid"]
            validade = request.json["validade"]
            status = request.json["status"]
            cadastrado_em = request.json["cadastrado_em"]
            atualizado_em = request.json["atualizado_em"]

            novo_mixproduto = mix_produto.Mixproduto(cliente=cliente, cod_prod_mix=cod_prod_mix, produto=produto, descricao=descricao,
                                                    modo_preparo=modo_preparo, departamento=departamento, rend_kg=rend_kg, rend_unid=rend_unid,
                                                    validade=validade, status=status, cadastrado_em=cadastrado_em, atualizado_em=atualizado_em)
            resultado = mix_produto_service.cadastrar_mixproduto(novo_mixproduto)
            x = ms.jsonify(resultado)
            return make_response(x, 201)

class MixprodutoDetail(Resource):
    def get(self, id):
        Mixproduto = mix_produto_service.listar_mixproduto_id(id)
        if Mixproduto is None:
            return make_response(jsonify("Mix de Produto não foi encontrado"), 404)
        ms = mix_produto_schema.MixprodutoSchema()
        return make_response(ms.jsonify(Mixproduto), 200)

    def put(self, id):
        mixproduto_bd = mix_produto_service.listar_mixproduto_id(id)
        if mixproduto_bd is None:
            return make_response(jsonify("Mix de Produto não foi encontrado"), 404)
        ms = mix_produto_schema.MixprodutoSchema()
        validate = ms.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            cliente = request.json["cliente"]
            cod_prod_mix = request.json["cod_prod_mix"]
            produto = request.json["produto"]
            descricao = request.json["descricao"]
            modo_preparo = request.json["modo_preparo"]
            departamento = request.json["departamento"]
            rend_kg = request.json["rend_kg"]
            rend_unid = request.json["rend_unid"]
            validade = request.json["validade"]
            status = request.json["status"]
            cadastrado_em = request.json["cadastrado_em"]
            atualizado_em = request.json["atualizado_em"]

            novo_mixproduto = mix_produto.Mixproduto(cliente=cliente, cod_prod_mix=cod_prod_mix, produto=produto, descricao=descricao,
                                                    modo_preparo=modo_preparo, departamento=departamento, rend_kg=rend_kg, rend_unid=rend_unid,
                                                    validade=validade, status=status, cadastrado_em=cadastrado_em, atualizado_em=atualizado_em)
            mix_produto_service.atualiza_mixproduto(mixproduto_bd, novo_mixproduto)
            mixproduto_atualizado = mix_produto_service.listar_mixproduto_id(id)
            return make_response(ms.jsonify(mixproduto_atualizado), 200)

    def delete(self, id):
        mixproduto_bd = mix_produto_service.listar_mixproduto_id(id)
        if mixproduto_bd is None:
            return make_response(jsonify("Mix de Produto não encontrada"), 404)
        mix_produto_service.remove_mixproduto(mixproduto_bd)
        return make_response('Mix de Produto excluído com sucesso', 204)

api.add_resource(MixprodutoList, '/mixprodutos')
api.add_resource(MixprodutoDetail, '/mixprodutos/<int:id>')