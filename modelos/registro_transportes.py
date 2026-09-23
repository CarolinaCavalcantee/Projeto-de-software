#RF9
class RegistroTransportes:
    def __init__(self):
        self._registros = {}
    def registrar(self, transporte) -> bool:
        chave = transporte.chave_identificacao()
        era_novo = chave not in self._registros
        self ._registros[chave] = transporte
        return era_novo
    def listar(self) -> list:
        return list(self._registros.values())
    def quantidade(self) -> int:
        return len(self._registros)