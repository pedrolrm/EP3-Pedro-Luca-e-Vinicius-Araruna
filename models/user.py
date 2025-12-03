import os 
from typing import List, Optional
from models.base_model import BaseModel

# User herda do BaseModel para ter acesso aos metodos comuns de CRUD
class User(BaseModel):
    #password com valor None para nao quebrar codigo antigo
    # birthdate ainda nao esta sendo salvo no banco
    def __init__(self, id, name, email, birthdate, password=None):
        super().__init__(id) #configurar ID no BaseModel
        self.id = id
        self.name = name
        self.email = email
        self.birthdate = birthdate
        self.password = password

    def __repr__(self):
        return (f"User(id={self.id}, name='{self.name}', email='{self.email}', "
                f"birthdate='{self.birthdate}')")
    
    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'birthdate': self.birthdate
        }
    
    @classmethod
    def from_dict(cls,data):
        return cls(
            id= data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            birthdate=data.get('birthdate'),
            password=data.get('password')
        )
    
# User model herda de BaseModel, para usar conexao SQLite
class UserModel(BaseModel):
    def __init__(self):
        # carrega lista inicial do banco 
        self.users = self._load()

    def _load(self) -> List[User]:
        """Carrega users do banco de dados ao inves do JSON"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Busca colunas e renomeia no SQL para nome -> name, password -> senha
        # Birthdate esta como vazio pois nao existe essa coluna no database ainda
        rows = cursor.execute('SELECT id, nome as name, email, senha as password FROM usuario').fetchall()
        conn.close()

        loaded_users = []
        for row in rows:
            user = User(
                id = row['id'],
                name = row['name'],
                email = row['email'],
                password = row['password'],
                birthdate = None
            )
            loaded_users.append(user)

        return loaded_users
        
    def _save(self):
        """
        SQLite os dados sao salvos instantaneamente no add/update/delete
        entao a funcao nao precisa fazer nada
        """
        pass

    def get_all(self) -> List[User]:
        # recarregar o banco 
        self.users = self._load()
        return self.users
        
    def get_by_id(self, user_id: int) -> Optional[User]:
        conn = self.get_connection()
        cursor = conn.cursor()
        row = cursor.execute('SELECT id, nome as name, email, senha as password FROM usuario WHERE id = ?', (user_id,)).fetchone()
        conn.close()

        if row:
            return User(id=row['id'], name=row['name'], email=row['email'], password=row['password'], birthdate=None)
        return None
        
    # funcao para login(procura pelo email)
    def get_by_email(self, email: str) -> Optional[User]:
        conn = self.get_connection()
        cursor = conn.cursor()
        row = cursor.execute('SELECT id, nome as name, email, senha as password FROM usuario WHERE email = ?', (email,)).fetchone()
        conn.close()

        if row:
            return User(id=row['id'], name=row['name'], email=row['email'], password=row['password'], birthdate=None)
        return None
        
    def add_user(self,user: User):
        conn = self.get_connection()
        cursor = conn.cursor()

        # insercao no SQL mapeando name -> nome e password -> senha
        cursor.execute('''
            INSERT INTO usuario (nome, email, senha )
            VALUES (?, ?, ?)
            ''', (user.name, user.email, user.password))
        
        conn.commit()

        #atualiza ID objeto com o ID gerado pelo Banco 
        user.id = cursor.lastrowid
        conn.close()
        #atualiza lista local 
        self.users.append(user)

    def update_user(self, update_user: User):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuario
            SET nome = ?, email = ?, senha = ?
            WHERE id = ?
            ''', (update_user.name, update_user.email, update_user.password, update_user.id ))
        
        conn.commit()
        conn.close()
        #atualiza lista local: substitui o objeto com mesmo id
        self.users = [update_user if u.id == update_user.id else u for u in self.users]

    def delete_user(self, user_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM usuario WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        #atualiza lista local removendo o user deletado
        self.users = [u for u in self.users if u.id != user_id]