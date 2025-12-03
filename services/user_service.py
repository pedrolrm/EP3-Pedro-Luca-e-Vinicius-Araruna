from bottle import request
from models.user import UserModel, User
from utils.password_utils import hash_password

class UserService:
    def __init__(self):
        self.user_model = UserModel()


    def get_all(self):
        return self.user_model.get_all()
    
    def get_by_id(self, user_id):
        return self.user_model.get_by_id(user_id)
    
    def get_by_email(self, email):
        return self.user_model.get_by_email(email)
    
    #Cria usuario vindo do registro sem depender do request
    def create_user(self,name,email,password):
        hashed_password = hash_password(password)
        user = User(id=None, name=name, email=email, password=hashed_password, birthdate=None)
        self.user_model.add_user(user)
        return user

    def save(self):
        name = request.forms.get('name')
        email = request.forms.get('email')
        birthdate = request.forms.get('birthdate')
        password = request.forms.get('password')
        # id = None faz o SQLite gerar o id 
        hashed_password = hash_password(password)
        user = User(id=None, name=name, email=email, birthdate=birthdate,  password= hashed_password)
        self.user_model.add_user(user)

    def edit_user(self, user):
        name = request.forms.get('name')
        email = request.forms.get('email')
        birthdate = request.forms.get('birthdate')

        user.name = name
        user.email = email
        user.birthdate = birthdate

        self.user_model.update_user(user)


    def delete_user(self, user_id):
        self.user_model.delete_user(user_id)
