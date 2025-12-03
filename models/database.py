import sqlite3
import os 

#caminho do banco de dados
DB_FOLDER = 'data'
DB_NAME = 'app_database.db'
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)

def get_db_connection():
    """ Conectar ao banco de dados SQLite"""
    conn = sqlite3.connect(DB_PATH)
    # para permitir acessar colunas a partir do nome, ao inves de indicie numerico 
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """ Cria as tabelas do sistema para caso elas nao existam"""
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute ("PRAGMA foreign_keys = ON;")

    print(f"Criando banco de dados em: {DB_PATH}")

    #user table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS usuario(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   senha TEXT NOT NULL 
               )
           ''')
    # category table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categoria(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   tipo TEXT NOT NULL
               ) 
           ''')

    # transaction table ( N-1 relation with user and category)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacao(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   valor REAL NOT NULL,
                   data TEXT NOT NULL,
                   descricao TEXT,
                   usuario_id INTEGER NOT NULL,
                   categoria_id INTEGER NOT NULL,
                   FOREIGN KEY (usuario_id) REFERENCES usuario(id),
                   FOREIGN KEY (categoria_id) REFERENCES categoria(id)
                )
          ''')
    
    #  Tabela de Recorrências 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recorrencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            categoria_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,          -- 'despesa' ou 'receita'
            valor REAL NOT NULL,
            descricao TEXT,
            frequencia TEXT NOT NULL,    -- 'mensal', 'semanal', 'anual'
            data_inicio TEXT NOT NULL,   -- Data do primeiro pagamento
            proxima_data TEXT NOT NULL,  -- Controle interno: quando lançar a próxima?
            ativo INTEGER DEFAULT 1,     -- 1 = Ativa, 0 = Cancelada
            FOREIGN KEY (usuario_id) REFERENCES usuario (id),
            FOREIGN KEY (categoria_id) REFERENCES categoria (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso.")

    # permite rodar esse arquivo diretamente para inicializar o banco de dados
if __name__ == '__main__':
    init_db() 