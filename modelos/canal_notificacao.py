from abc import ABC, abstractmethod

class CanalNotificacao(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, mensagem: str) -> None:
        raise NotImplementedError


class CanalEmail(CanalNotificacao):
    def enviar(self, destinatario: str, mensagem: str) -> None:
        print(f"[E-mail para {destinatario}] {mensagem}")


class CanalPush(CanalNotificacao):
    def enviar(self, destinatario: str, mensagem: str) -> None:
        print(f"[Push para {destinatario}] {mensagem}")