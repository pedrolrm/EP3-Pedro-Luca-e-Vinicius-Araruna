from models.database import get_db_connection

class BaseModel:
    """
    Classe Pai para garantir Heranca e conexao com o banco de dados SQLite
    """
    def __init__(self, id=None):
        self.id = id

    @classmethod
    def get_connection(cls):
        """ Retorna conexao com o banco de dados SQLite """
        return get_db_connection()
    @classmethod
    def buscar_todos(cls,tabela):
        #metodo para buscar tudo de uma tabela
        conn = cls.get_connection()
        registros = conn.execute(f'SELECT * FROM {tabela}').fetchall()
        conn.close()
        return [dict(row) for row in registros]