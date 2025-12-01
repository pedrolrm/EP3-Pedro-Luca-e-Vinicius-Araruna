from bottle import Bottle, request, response
from .base_controller import BaseController
from models.user import UserModel, User

class UserController(BaseController):
    def __init__(self, app):
        super().__init__(app)

        self.setup_routes()
        self.user_service = UserModel()


    # Rotas User
    def setup_routes(self):
        #rotas de autenticação
        self.app.route('/cadastro', method=['GET', 'POST'], callback=self.registrar)
        self.app.route('/login', method=['GET'], callback=self.login_view)

        self.app.route('/users', method='GET', callback=self.list_users)
        self.app.route('/users/add', method=['GET', 'POST'], callback=self.add_user)
        self.app.route('/users/edit/<user_id:int>', method=['GET', 'POST'], callback=self.edit_user)
        self.app.route('/users/delete/<user_id:int>', method='POST', callback=self.delete_user)

    def registrar(self):
        if request.method == 'GET':
            return self.render('views/register.html', erro=None)
        elif request.method == 'POST':
            nome = request.forms.get('nome')
            email = request.forms.get('email')
            senha = request.forms.get('senha')

            if self.user_service.get_by_email(email):
                return self.render('views/register.html', erro= "Email ja cadastrado!")
            
            try:
                novo_user = User(id=None, name=nome, email=email, password=senha, birthdate=None)
                self.user_service.add_user(novo_user)

                print(f"Usuário {nome} cadastrado com sucesso!")
                return self.redirect('/login')
            except Exception as e:
                return self.render('views/register.html', erro=f"Erro: {str(e)}")

    def login_view(self):
        if request.method == 'GET':
            return self.render('views/login.html', erro=None)
                
        elif request.method == 'POST':
            email = request.forms.get('email')
            senha = request.forms.get('senha')
            user = self.user_service.get_by_email(email)
            if user and user.password == senha:
                response.set_cookie("user_id", str(user.id), secret='sua_chave_secreta_aqui')
                print(f"Usuário {user.name} logado com sucesso.")
                return self.redirect('/dashboard')
            else:
                return self.render('views/login.html', erro="E-mail ou senha incorretos.")
    
    def logout(self):
        # Remove o cookie para sair
        response.delete_cookie("user_id")
        return self.redirect('/login')

    def list_users(self):
        users = self.user_service.get_all()
        return self.render('users', users=users)


    def add_user(self):
        if request.method == 'GET':
            return self.render('user_form', user=None, action="/users/add")
        else:
            # POST - salvar usuário
            self.user_service.save()
            self.redirect('/users')


    def edit_user(self, user_id):
        user = self.user_service.get_by_id(user_id)
        if not user:
            return "Usuário não encontrado"

        if request.method == 'GET':
            return self.render('user_form', user=user, action=f"/users/edit/{user_id}")
        else:
            # atualiza o objeto com dados do form
            user.name = request.forms.get('name')
            user.email = request.forms.get('email')
            # POST - salvar edição
            self.user_service.edit_user(user)
            self.redirect('/users')


    def delete_user(self, user_id):
        self.user_service.delete_user(user_id)
        self.redirect('/users')


user_routes = Bottle()
user_controller = UserController(user_routes)
