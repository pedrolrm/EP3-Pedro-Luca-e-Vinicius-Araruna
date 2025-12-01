from bottle import request, response
import json
from services.transacao_service import TransacaoService
from .base_controller import BaseController
from utils.auth_middleware import require_auth

class TransacaoController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.service = TransacaoService()
        self.setup_routes()

    def _json_response(self, data, status=200):
        response.status = status
        response.content_type = 'application/json'
        return json.dumps(data)

    def setup_routes(self):
        self.app.route('/transacoes', method='GET', callback=require_auth(self.list_transacoes_by_user))
        self.app.route('/transacoes', method='POST', callback=require_auth(self.create_transacao))
        self.app.route('/transacoes/<transacao_id>', method='PUT', callback=require_auth(self.update_transacao))
        self.app.route('/transacoes/<transacao_id>', method='DELETE', callback=require_auth(self.delete_transacao))

    def list_transacoes_by_user(self):
        transacoes = self.service.get_transacao_by_user(request.user_id)
        return self._json_response(transacoes)

    def create_transacao(self):
        data = request.json
        if not data or 'valor' not in data or 'categoria_id' not in data:
            return self._json_response({'error': 'Dados incompletos para criar a transação.'}, status=400)
        
        new_id = self.service.create_transacao(
            usuario_id=request.user_id,
            categoria_id=data['categoria_id'],
            valor=data['valor'],
            data=data['data'],
            descricao=data.get('descricao', '')
        )

        if new_id:
            return self._json_response({'message': 'Transação criada com sucesso.', 'transacao_id': new_id}, status=201)
        else:
            return self._json_response({'error': 'Ocorreu um erro ao criar a transação.'}, status=500)

    def update_transacao(self, transacao_id):
        data = request.json
        if not data:
            return self._json_response({'error': 'Dados incompletos para atualizar a transação.'}, status=400)
        
        success = self.service.update_transacao(
            transacao_id=transacao_id,
            usuario_id=request.user_id,
            valor=data.get('valor'),        
            data=data.get('data'),
            descricao=data.get('descricao'),
            categoria_id=data.get('categoria_id') 
        )
        
        if success:
            return self._json_response({'message': "Transação atualizada com sucesso."})
        else:
            return self._json_response({'error': 'Ocorreu um erro ao atualizar a transação.'}, status=500)

    def delete_transacao(self, transacao_id):
        success = self.service.delete_transacao(transacao_id, request.user_id)
        
        if success:
            return self._json_response({'message': 'Transação deletada com sucesso.'})
        else:
            return self._json_response({'error': 'Ocorreu um erro ao deletar a transação.'}, status=500)