from bottle import static_file, template as bottle_template, HTTPResponse, response as bottle_response, request
# Importação necessária para verificar o token
from services.auth_service import AuthService

class BaseController:
    def __init__(self, app):
        self.app = app
        self._setup_base_routes()

    def _setup_base_routes(self):
        """Configura rotas básicas comuns a todos os controllers"""
        self.app.route('/', method='GET', callback=self.home_redirect)
        self.app.route('/helper', method=['GET'], callback=self.helper)

        # Rota para arquivos estáticos (CSS, JS, imagens)
        self.app.route('/static/<filename:path>', callback=self.serve_static)

    def home_redirect(self):
        """
        Redireciona para a Home Page.
        Lógica inteligente: Verifica se o usuário já está logado para adaptar a tela.
        """
        user_name = None
        
        # Tenta pegar o cookie de autenticação
        token = request.get_cookie("auth_token")
        
        if token:
            # Se o cookie existe, validamos se o token é verdadeiro
            payload = AuthService.validate_token(token)
            
            if payload:
                # Se for válido, extraímos o nome do usuário
                user_name = payload['name']

        # O HTML vai usar esse 'user_name' no %if para decidir quais botões mostrar
        return self.render('views/home.html', user_name=user_name)

    def helper(self):
        return self.render('helper-final')

    def serve_static(self, filename):
        """Serve arquivos estáticos da pasta static/"""
        return static_file(filename, root='./static')

    def render(self, template_name, **context):
        """Método auxiliar para renderizar templates"""
        from bottle import template as render_template
        return render_template(template_name, **context)

    def redirect(self, path, code=302):
        """Redirecionamento robusto com tratamento de erros"""
        try:
            bottle_response.status = code
            bottle_response.set_header('Location', path)
            return bottle_response
        except Exception as e:
            print(f"ERRO NO REDIRECT: {type(e).__name__} - {str(e)}")
            return HTTPResponse(
                body=f'<script>window.location.href="{path}";</script>',
                status=200,
                headers={'Content-Type': 'text/html'}
            )