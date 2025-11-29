import sqlite3
from models.database import get_db_connection

class TransacaoService:

    def create_transacao(self, usuario_id, categoria_id, valor, data, descricao):
        conn = get_db_connection() # Abre conexao com o banco de dados
        cursor = conn.cursor() # Cria um cursor para executar comandos SQL
        try:

            cursor.execute('''
                INSERT INTO transacao (valor, data, descricao, usuario_id, categoria_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (valor, data, descricao, usuario_id, categoria_id))
            conn.commit()
            new_id = cursor.lastrowid # Retorna o ID da nova transacao criada
            return new_id
        except sqlite3.Error as e:
            print(f"Ocorreu um erro ao criar a transacao: {e}")
            return None
        finally:
            conn.close()
    
    def get_transacao_by_user(self, usuario_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                t.id, t.valor, t.data, t.descricao, 
                c.nome as categoria_nome, c.tipo as tipo_transacao
            FROM transacao t
            INNER JOIN categoria c ON t.categoria_id = c.id
            WHERE t.usuario_id = ?
            ORDER BY t.data DESC
        """
        try:
            cursor.execute(query, (usuario_id,))
            transacoes = [dict(row) for row in cursor.fetchall()] # Converte cada linha em um dicionario
            return transacoes
        except sqlite3.Error as e:
            print(f"Ocorreu um erro ao buscar transacoes: {e}")
            return None
        finally:
            conn.close()
    
    def update_transacao(self, transacao_id, valor, data, descricao, categoria_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE transacao
                SET valor = ?, data = ?, descricao = ?, categoria_id = ?
                WHERE id = ?
            ''', (valor, data, descricao, categoria_id, transacao_id))
            conn.commit()
            return cursor.rowcount > 0  # Retorna True se alguma linha foi atualizada
        except sqlite3.Error as e:
            print(f"Ocorreu um erro ao atualizar a sua transacao: {e} ")
            return None
        finally:
            conn.close()

    def delete_transacao(self, transacao_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM transacao WHERE id = ? AND usuario_id = ?', (transacao_id,)) # Confirmando que o usuário está deletando a sua própria transação
            conn.commit()
            return cursor.rowcount > 0  # Retorna True se alguma linha foi deletada
        except sqlite3.Error as e:
            print(f"Ocorreu um erro ao deletar a transacao: {e}")
            return False
        finally:
            conn.close()