import datetime
from functools import wraps
from flask import request, jsonify, Response
import jwt


def token_required(f:object) -> str:
    @wraps(f)
    def token(*args:object, **kwargs:object) -> object:
        data = request.json
        if not data:
            return Response("Não autenticado", status=401, mimetype='application/json')
        else:
            try:
                data = jwt.decode(data['token'], "teste")
            except Exception as e:
                print(e)
                return Response("Não autenticado", status=401, mimetype='application/json')

        return f(data, *args, **kwargs)
    return token


def oauth(user:str) -> jsonify:
    token = jwt.encode({'name': user, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12) },
                           "teste")
    return jsonify({'message': 'generate token', 'token': token.decode('UTF-8'),
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=12)})