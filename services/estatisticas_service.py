import sqlite3
from models.database import get_db_connection
from datetime import datetime

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
    
    def get_resumo_financeiro(self, usuario_id, mes=None, ano=None):
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
                SELECT 
                    SUM(CASE WHEN c.tipo = 'receita' THEN t.valor ELSE 0 END) as total_receitas,
                    SUM(CASE WHEN c.tipo = 'despesa' THEN t.valor ELSE 0 END) as total_despesas
                FROM transacao t
                JOIN categoria c ON t.categoria_id = c.id
                WHERE t.usuario_id = ?
            """
            params = [usuario_id]

            # Se passou mês e ano, adiciona filtro de data
            if mes and ano:
                query += " AND strftime('%m', t.data) = ? AND strftime('%Y', t.data) = ?"
                params.extend([mes, ano])

            try:
                cursor.execute(query, params)
                row = cursor.fetchone()

                receitas = row['total_receitas'] or 0.0
                despesas = row['total_despesas'] or 0.0
                
                return {
                    "receitas": receitas,
                    "despesas": despesas,
                    "saldo": receitas - despesas
                }
            except sqlite3.Error as e:
                print(f"Erro ao calcular resumo: {e}")
                return {"receitas": 0.0, "despesas": 0.0, "saldo": 0.0}
            finally:
                conn.close()