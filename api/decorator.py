from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import make_response, jsonify

#TODO método para controle de usuários E PERMISSÕES Admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['roles'] != 'admin':
            return make_response(jsonify(mensagem='Não e permitido esse recurso. Apenas administradores'), 403)
        else:
            return fn(*args, **kwargs)
    return wrapper