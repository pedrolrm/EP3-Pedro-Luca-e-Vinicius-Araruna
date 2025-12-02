from models.base_model import BaseModel

class Recorrencia(BaseModel):
    def __init__(self, id=None, usuario_id=None, categoria_id=None, tipo=None,
                  valor=0.0, descricao=None, frequencia= 'mensal', data_inicio=None,
                    proxima_data=None, ativo=1):
        super.__init__(id)
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

    