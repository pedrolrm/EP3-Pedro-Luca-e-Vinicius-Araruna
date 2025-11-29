class Transacao:
    def __init__(self, id, valor, data, descricao, usuario_id, categoria_id, categoria_nome=None, tipo_transacao=None):
        self.id = id
        self.valor = valor
        self.data = data
        self.descricao = descricao
        self.usuario_id = usuario_id
        self.categoria_id = categoria_id
        self.categoria_nome = categoria_nome
        self.tipo_transacao = tipo_transacao

    def to_dict(self):
        """ Converte o objeto para dicionário (necessário para o Bottle gerar o JSON) """
        data = {
            'id': self.id,
            'valor': self.valor,
            'data': self.data,
            'descricao': self.descricao,
            'usuario_id': self.usuario_id,
            'categoria_id': self.categoria_id,
            'categoria_nome': self.categoria_nome,
            'tipo_transacao': self.tipo_transacao
        }

        if self.categoria_nome: # Adiciona ao JSON apenas se nao for None
            data["categoria_nome"] = self.categoria_nome
        if self.tipo_transacao:
            data["tipo_transacao"] = self.tipo_transacao
            
        return data