from flask_restful import Resource
from api import api
from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta

class RefreshTokenList(Resource):
    @jwt_required(refresh=True)
    def post(self):
        usuario_token = get_jwt_identity()
        access_token = create_access_token(
            identity=usuario_token,
            expires_delta=timedelta(seconds=100)
        )
        refresh_token = create_refresh_token(
            identity=usuario_token
        )

        return make_response({
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200)

api.add_resource(RefreshTokenList, '/token/refresh')
