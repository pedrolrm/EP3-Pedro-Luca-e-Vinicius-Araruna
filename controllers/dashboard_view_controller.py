from bottle import request, redirect
from .base_controller import BaseController
from utils.auth_middleware import require_auth 
from services.recorrencia_service import RecorrenciaService

class DashboardViewController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.recorrencia_service = RecorrenciaService()
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/dashboard', method='GET', callback=self.view_dashboard)

    @require_auth
    def view_dashboard(self):
        user_id = request.user_id # @require_auth garante que o request_user.id existe

        #verifica algo atrasado
        novas_transacoes = self.recorrencia_service.processar_recorrencia(user_id)
        mensagem = None
        if novas_transacoes > 0 :
            mensagem = f"{novas_transacoes} transações recorrentes foram lançadas automaticamente!"
            #aqui busca o saldo real
            
        # Renderiza o HTML e passa o nome do usuário logado
        return self.render('views/dashboard.html', user_name=request.user_name, msg=mensagem)
