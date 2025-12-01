from bottle import request, redirect
from .base_controller import BaseController
from utils.auth_middleware import require_auth 

class DashboardViewController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/dashboard', method='GET', callback=self.view_dashboard)

    @require_auth
    def view_dashboard(self):
        # Renderiza o HTML e passa o nome do usuário logado
        return self.render('views/dashboard.html', user_name=request.user_name)