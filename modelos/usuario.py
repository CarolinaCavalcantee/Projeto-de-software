class UsuarioInscrito:
    def __init__(self, nome: str, inscricoes: list):
        if not inscricoes:
            raise ValueError(
                f"Usuário '{nome}' precisa de pelo menos um canal de notificação."
            )
        self.nome = nome
        self.inscricoes = inscricoes