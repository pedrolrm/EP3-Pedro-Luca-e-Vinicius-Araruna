from bottle import request
from models.user import UserModel, User

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
        user = User(id=None, name=name, email=email, password=password, birthdate=None)
        self.user_model.add_user(user)
        return user



    def save(self):
        last_id = max([u.id for u in self.user_model.get_all()], default=0)
        new_id = last_id + 1
        name = request.forms.get('name')
        email = request.forms.get('email')
        birthdate = request.forms.get('birthdate')

        user = User(id=new_id, name=name, email=email, birthdate=birthdate)
        self.user_model.add_user(user)


    def get_by_id(self, user_id):
        return self.user_model.get_by_id(user_id)


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
