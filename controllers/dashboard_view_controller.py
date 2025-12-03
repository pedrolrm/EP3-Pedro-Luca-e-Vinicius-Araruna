from bottle import request, redirect, template
from .base_controller import BaseController
from utils.auth_middleware import require_auth 
from services.recorrencia_service import RecorrenciaService
from services.transacao_service import TransacaoService

class DashboardViewController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.recorrencia_service = RecorrenciaService()
        self.transacao_service = TransacaoService()
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/dashboard', method='GET', callback=self.view_dashboard)

    @require_auth
    def view_dashboard(self):
        user_id = request.user_id # @require_auth garante que o request_user.id existe

        lista_transacoes = self.transacao_service.get_transacao_by_user(user_id)
        lista_recorrencias = self.recorrencia_service.processar_recorrencia(user_id)


        return template(
            'views/dashboard',  
            transacoes=lista_transacoes,
            recorrencias=lista_recorrencias,
            user_name=request.user_name, 
            msg = f"{lista_recorrencias} Transações recorrentes foram processadas automaticamente." if lista_recorrencias > 0 else None
        )
