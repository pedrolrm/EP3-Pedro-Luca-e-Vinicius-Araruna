from bottle import request, response
import json
from services.estatisticas_service import EstatisticasService
from .base_controller import BaseController
from utils.auth_middleware import require_auth

class EstatisticasController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.service = EstatisticasService()
        self.setup_routes()

    def _json_response(self, data, status=200):
        response.status = status
        response.content_type = 'application/json'
        return json.dumps(data)

    def setup_routes(self):
        # Resumo Financeiro
        self.app.route('/estatisticas/resumo', method='GET', callback=require_auth(self.get_resumo))

        # Distribuição por Categoria 
        self.app.route('/estatisticas/categorias', method='GET', callback=require_auth(self.get_por_categoria))

        #Evolução Mensal 
        self.app.route('/estatisticas/evolucao', method='GET', callback=require_auth(self.get_evolucao))

        # Rota Combo 
        self.app.route('/estatisticas/dashboard', method='GET', callback=require_auth(self.get_dashboard_completo))

    def get_resumo(self):
        mes = request.query.mes
        ano = request.query.ano
        
        mes = mes if mes else None # Transforma mes em nome se vier vazio
        ano = ano if ano else None # Transforma ano em nome se vier vazio

        dados = self.service.get_resumo_financeiro(request.user_id, mes, ano)
        return self._json_response(dados)

    def get_por_categoria(self):
        mes = request.query.mes
        ano = request.query.ano
        tipo = request.query.tipo or 'despesa' 

        mes = mes if mes else None
        ano = ano if ano else None

        dados = self.service.get_total_por_categoria(request.user_id, tipo, mes, ano)
        return self._json_response(dados)

    def get_evolucao(self):
        try:
            limite = int(request.query.limite)
        except:
            limite = 12

        dados = self.service.get_evolucao_mensal(request.user_id, limite)
        return self._json_response(dados)

    def get_dashboard_completo(self): # Rota combo que chama as 3 estatiscsa de uma vez
        mes = request.query.mes
        ano = request.query.ano
        mes = mes if mes else None
        ano = ano if ano else None

        resumo = self.service.get_resumo_financeiro(request.user_id, mes, ano)
        grafico_pizza = self.service.get_total_por_categoria(request.user_id, 'despesa', mes, ano)
        grafico_evolucao = self.service.get_evolucao_mensal(request.user_id, 12)

        return self._json_response({
            "resumo": resumo,
            "grafico_pizza": grafico_pizza,
            "grafico_evolucao": grafico_evolucao
        })