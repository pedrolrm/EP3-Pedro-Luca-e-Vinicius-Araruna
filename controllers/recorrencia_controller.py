from bottle import request,redirect
from controllers.base_controller import BaseController
from utils.auth_middleware import require_auth
from models.recorrencia import Recorrencia
from models.categoria import Categoria

class RecorrenciaController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/recorrencias', method='GET', callback= self.listar)
        self.app.route('/recorrencias/nova', method='POST', callback = self.salvar)
        self.app.route('/recorrencia/delete/<id:int>', method='GET', callback=self.excluir)

    @require_auth
    def listar(self):
        user_id = request.user_id

        #busca os dados para mostrar na tela 
        recorrencias = Recorrencia.buscar_ativas_por_usuario(user_id)
        categorias = Categoria.buscar_todas() # para o select do formulario

        return self.render('views/recorrencias.html',
                           user_name=request.user_name,
                           recorrencias=recorrencias,
                           categorias=categorias)
    
    @require_auth
    def salvar(self):
        # bloco de try catch para pegar os dados do formulario e criar objeto
        try:
            user_id = request.user_id
            descricao = request.forms.get('descricao')
            valor = float(request.forms.get('valor'))
            categoria_id = int(request.forms.get('categoria_id'))
            tipo = request.forms.get('tipo')
            frequencia = request.forms.get('frequencia')
            data_inicio = request.forms.get('data_inicio')

            nova = Recorrencia(
                usuario_id= user_id,
                categoria_id= categoria_id,
                tipo= tipo,
                valor= valor,
                descricao= descricao,
                frequencia= frequencia,
                data_inicio= data_inicio,
                proxima_data= data_inicio,
                ativo= 1
            )
            nova.salvar()

            print(f"✅ Recorrência '{descricao}' criada!")
        except Exception as e:
            print(f"❌ Erro ao salvar recorrência: {e}")

        #volta para a lista
        return redirect('/recorrencias')
    
    @require_auth
    def excluir(self):
        conn = Recorrencia.get_connection()
        conn.execute("DELETE FROM recorrencia WHERE id = ?" , (id,))
        conn.commit()
        conn.close()

        return redirect('/recorrencias')