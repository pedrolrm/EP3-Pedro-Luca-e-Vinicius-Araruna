from bottle import Bottle, request, response
import json
from services.transacao_service import TransacaoService

transacao_app = Bottle()
service = TransacaoService()

def json_response(data, status=200): # Helper para formatar respostas JSON
    response.status = status
    response.content_type = 'application/json'
    return json.dumps(data)

@transacao_app.route('/', method='GET') # Listar
def list_transacoes_by_user():
    transacoes = service.get_transacao_by_user(request.query.usuario_id)
    return json_response(transacoes)

@transacao_app.route('/', method='POST') # Criar
def create_transacao(): 
    data = request.json
    if not data or 'valor' not in data or 'usuario_id' not in data or 'categoria_id' not in data:
        return json_response({'error': 'Dados incompletos para criar a transação.'}, status=400)
    
    new_id = service.create_transacao(
        usuario_id=data['usuario_id'],
        categoria_id=data['categoria_id'],
        valor=data['valor'],
        data=data['data'],
        descricao=data.get('descricao', '')
    )

    if new_id:
        return json_response({'message': 'Transação criada com sucesso.', 'transacao_id': new_id}, status=201)
    else:
        return json_response({'error': 'Ocorreu um erro ao criar a transação.'}, status=500)
    
@transacao_app.route('/<transacao_id>', method='PUT') # Atualizar
def update_transacao(transacao_id):
    data = request.json
    if not data:
        return json_response({'error': 'Dados incompletos para atualizar a transação.'}, status=400)
    success = service.update_transacao(
        transacao_id=transacao_id,
        usuario_id=data.get('user_id'),
        valor=data.get('valor'),        
        data=data.get('data'),
        descricao=data.get('descricao'),
        categoria_id=data.get('categoria_id') 
    )
    if success:
        return json_response({'message': "Transação atualizada com sucesso."})
    else:
        return json_response({'error': 'Ocorreu um erro ao atualizar a transação.'}, status=500)
    
@transacao_app.route('/<transacao_id>',  method='DELETE') # Deletar
def delete_transacao(transacao_id):
    data = request.json
    success = service.delete_transacao(transacao_id, data.get('user_id'))
    if success:
        return json_response({'message': 'Transação deletada com sucesso.'})
    else:
        return json_response({'error': 'Ocorreu um erro ao deletar a transação.'}, status=500)