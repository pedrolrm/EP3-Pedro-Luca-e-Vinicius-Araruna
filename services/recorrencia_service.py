from datetime import datetime, timedelta
from models.recorrencia import Recorrencia
from models.transacao import Transacao

class RecorrenciaService:
    def processar_recorrencia(self, usuario_id):
        """
        verifica as recorrencias ativas e gera a transacao se a data chegou
        retorna o numero de transacoes geradas
        """
        hoje = datetime.now().date()

        #busca as recorrencias ativas
        recorrencias = Recorrencia.buscar_ativas_por_usuario(usuario_id)
        count_geradas = 0

        for rec in recorrencias:
            # usar um try catch para converter a string yyyy-mm-dd do banco para objeto
            try:
                data_agendada = datetime.strptime(rec.proxima_data, '%Y-%m-%d').date()
            except ValueError:
                continue # para pular se a data tiver invalida
                
                # esta atrasada?
            if data_agendada <= hoje:
                print(f"Processando recorrência: {rec.descricao} ({rec.proxima_data})")

                # criar transacao auto
                nova_transacao = Transacao(
                    id=None,
                    usuario_id=usuario_id,
                    categoria_id=rec.categoria_id,
                    tipo = rec.tipo,
                    valor= rec.valor,
                    descricao= f"[Automático] {rec.descricao}",
                    data= rec.proxima_data
                )
                nova_transacao.salvar()

                nova_proxima_data = self._calcular_proxima_data(data_agendada,rec.frequencia)
                rec.atualizar_proxima_data(nova_proxima_data)
                count_geradas +=1

        return count_geradas
        
    def _calcular_proxima_data(self, data_atual, frequencia):
        #calcula nova data com base na frequencia
        if frequencia == 'semanal':
            return(data_atual + timedelta(weeks=1)).strftime('%Y-%m-%d')
        elif frequencia == 'mensal':
            return(data_atual + timedelta(days=30)).strftime('%Y-%m-%d')
        elif frequencia == 'anual':
            return(data_atual + timedelta(days=365)).strftime('%Y-%m-%d')
        
        return (data_atual + timedelta(days=1)).strftime('%Y-%m-%d')


