from models.base_model import BaseModel
import sqlite3

class Recorrencia(BaseModel):
    def __init__(self, id=None, usuario_id=None, categoria_id=None, tipo=None,
                  valor=0.0, descricao=None, frequencia= 'mensal', data_inicio=None,
                    proxima_data=None, ativo=1):
        super().__init__(id)
        self.usuario_id = usuario_id
        self.categoria_id = categoria_id
        self.tipo = tipo
        self.valor = valor
        self.descricao = descricao
        self.frequencia = frequencia
        self.data_inicio = data_inicio
        self.proxima_data = proxima_data
        self.ativo = ativo

    def salvar(self):
        #salvar recorrencia no banco de dados
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO recorrencia (usuario_id, categoria_id, tipo, valor, descricao, frequencia, data_inicio, proxima_data, ativo)
            VALUES (?,?,?,?,?,?,?,?,?)
        ''', (self.usuario_id, self.categoria_id, self.tipo, self.valor, self.descricao, self.frequencia, self.data_inicio, self.proxima_data, self.ativo))
        
        conn.commit()
        self.id = cursor.lastrowid
        cursor = conn.cursor()

    def atualizar_proxima_data(self, nova_data):
        # atualiza a data do proximo lancamento, usado depois de gerar transacao
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE recorrencia
            SET proxima_data = ?
            WHERE id = ?
        ''', (nova_data, self.id))

        conn.commit()
        conn.close()
        self.proxima_data = nova_data

    @classmethod
    def buscar_ativas_por_usuario(cls, usuario_id):
        # busca todas as recorrencias ativas de um user 
        conn = cls.get_connection()
        conn.row_factory = sqlite3.Row #garante o acesso por nome da coluna 
        cursor = conn.cursor()

        rows = cursor.execute('SELECT * FROM recorrencia WHERE usuario_id = ? AND ativo = 1', (usuario_id,)).fetchall()
        conn.close()

        lista_recorrencia = []   #converte as linhas do banco em objetos recorrencia
        for row in rows:
            dados = dict(row)
            lista_recorrencia.append(cls(**dados))

        return lista_recorrencia
    