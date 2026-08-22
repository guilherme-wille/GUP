from functools import wraps
from flask import session, jsonify


def login_required(f):
    """Antes redirecionava para a tela de login (Jinja).
    Agora, como o front é uma API consumida via fetch, devolvemos
    um JSON com status 401 para o frontend decidir o que fazer
    (por exemplo, redirecionar o usuário para a página de login)."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            return jsonify({"erro": "Você precisa estar logado para acessar essa rota."}), 401
        return f(*args, **kwargs)
    return wrapper


def familia_required(f):
    """Antes redirecionava para o dashboard (Jinja).
    Agora devolve 403 em JSON quando o usuário não faz parte de uma família."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('tem_familia'):
            return jsonify({"erro": "Você precisa fazer parte de uma família para acessar esta rota."}), 403
        return f(*args, **kwargs)
    return wrapper
