from modelos.usuario import UsuarioInscrito


#rf10
class Notificador:
    def __init__(self):
        self._inscritos: list[UsuarioInscrito] = []
    
    def inscrever(self, usuario: UsuarioInscrito) -> None:
        self._inscritos.append(usuario)
    def notificar_atraso(self, transporte) ->None:
        atraso = transporte.calcular_atraso()
        if atraso <= 0:
            return

        mensagem = f"Atraso detectado - {transporte.exibir_status()}"

        for usuario in self._inscritos:
            for canal, destinatario in usuario.inscricoes:
                canal.enviar(destinatario, mensagem)