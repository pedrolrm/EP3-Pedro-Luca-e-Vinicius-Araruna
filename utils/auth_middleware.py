from functools import wraps
from bottle import request,redirect
from services.auth_service import AuthService

def require_auth(callback):
    #decorator para proteger rotas com JWT
    @wraps(callback)
    def wrapper(*args,**kwargs):
        # tenta pegar o token do cookie
        token = request.get_cookie("auth_token")

        if not token:
            return redirect('/login')

        #valida o token
        payload = AuthService.validate_token(token)
        if not payload:
            return redirect('/login')
        
        # injeta dados do user na requisicao
        request.user_id = payload['sub']
        request.user_name = payload['name']

        return callback(*args,**kwargs)
    return wrapper