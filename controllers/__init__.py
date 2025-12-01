from bottle import Bottle
from controllers.user_controller import UserController
from controllers.auth_controller import AuthController
from controllers.base_controller import BaseController
from controllers.transacao_controller import TransacaoController

def init_controllers(app: Bottle):
    """
    Inicializa todos os controladores
    Ao instanciar a classe o __init__ dela ja registra as rotas no app
    """
    print('Carregando rotas...')

    #BaseController home e arquivos estaticos
    BaseController(app)
    #AuthController login, registro, logout
    AuthController(app)
    #UserController dashboard, CRUD adm
    UserController(app)
    #TransacaoController CRUD transacoes
    TransacaoController(app)

    print('Rotas registradas com sucesso!')
