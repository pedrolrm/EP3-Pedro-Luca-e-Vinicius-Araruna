from models.base_model import BaseModel
import sqlite3

class Categoria(BaseModel):
    def __init__(self, id=None, nome=None, tipo=None):
        super().__init__(id)
        self.nome = nome
        self.tipo = tipo

    def salvar(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO categoria (nome, tipo)
            VALUES (?, ?)
        """, (self.nome, self.tipo))

        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    @classmethod
    def buscar_todas(cls):
        #busca todas as categorias para preencher selects
        conn = cls.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        rows = cursor.execute("SELECT * FROM categoria").fetchall()
        conn.close()

        # converte as linhas do banco em objetos Categoria
        categorias = []
        for row in rows:
            dados = dict(row)
            categorias.append(cls(**dados))
        return categorias
    
    @classmethod
    def buscar_por_id(cls, id):
        conn = cls.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        row = cursor.execute("SELECT * FROM categoria WHERE id = ?", (id,)).fetchone()
        conn.close()

        if row:
            return cls(**dict(row))
        return None