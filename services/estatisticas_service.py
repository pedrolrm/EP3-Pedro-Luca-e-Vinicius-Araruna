import sqlite3
from models.database import get_db_connection

class EstatisticasService:
    
    def get_total_por_categoria(self, usuario_id, mes=None, ano=None):
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT c.nome as categoria, c.tipo, SUM(t.valor) as total
            FROM transacao t
            JOIN categoria c ON t.categoria_id = c.id
            WHERE t.usuario_id = ?
        """
        params = [usuario_id]
        
        if mes and ano:
            query += " AND strftime('%m', t.data) = ? AND strftime('%Y', t.data) = ?"
            params.extend([mes, ano])
        
        query += " GROUP BY c.nome, c.tipo ORDER BY total DESC"
        
        try:
            cursor.execute(query)
            resultados = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar estatísticas: {e}")
            resultados = []
        finally:
            conn.close()
        return resultados