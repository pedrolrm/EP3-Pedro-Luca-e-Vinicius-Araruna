from bottle import request, response, redirect
from controllers.base_controller import BaseController
from services.auth_service import AuthService
from services.user_service import UserService

class AuthController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.auth_service = AuthService()
        self.user_service = UserService()
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/login', method=['GET', 'POST'], callback=self.login)
        self.app.route('/register', method=['GET', 'POST'], callback=self.register)
        self.app.route('/logout', method='GET', callback=self.logout)

    def login(self):
        if request.method == 'GET':
            return self.render('views/login.html', erro=None)
        
        #POST
        email = request.forms.get('email')
        senha = request.forms.get('senha')

        token = self.auth_service.login(email,senha)
        if token:
            response.set_cookie("auth_token",token, httponly=True)
            return redirect('/dashboard')
        else:
            return self.render('views/login.html', erro="Email ou senha inválidos.")
        
    def register(self):
        if request.method == 'GET':
            return self.render('views/register.html', erro= None)
        
        #POST
        nome = request.forms.get('nome')
        email= request.forms.get('email')
        senha= request.forms.get('senha')

        #validacao:
        if self.user_service.get_by_email(email):
            return self.render('views/register.html', erro= "Email já cadastrado!")
        
        try:
            self.user_service.create_user(nome,email,senha)
            return redirect('/login')
        except Exception as e:
            return self.render('views/register.html', erro = str(e))
        
    def logout(self):
        response.delete_cookie("auth_token")
        return redirect('/login')