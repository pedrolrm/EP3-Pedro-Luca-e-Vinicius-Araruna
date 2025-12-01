import jwt
import time 
from services.user_service import UserService

#chaves para assinar o token
SECRET_KEY = "minha_chave_secreta_fincapp"
ALGORITHM = "HS256"

class AuthService:
    def __init__(self):
        #auth service usa o User service para buscar dados
        self.user_service = UserService()

    def login(self, email, senha):
        user = self.user_service.get_by_email(email) #busca user pelo email
        #validacao de senha
        if user and user.password == senha:
            return self._generate_token(user.id, user.name)
        
        return None
    
    def _generate_token(self, user_id, user_name):
        """GERA HASH JWT"""
        payload = {
            "sub": str(user_id), #id do user
            "name": user_name,#nome
            "iat": int(time.time()), #data de criacao
            "exp": int(time.time()) + 3600 #expirar em 1 hora
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def validate_token(token):
        """decodifica e valida o token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except(jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None