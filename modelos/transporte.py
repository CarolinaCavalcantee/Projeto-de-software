class Transporte:
    def __init__(self, origem, destino, retrato_horario, status):
        self.origem = origem
        self.destino = destino
        self.retrato_horario = retrato_horario
        self.status = status

    def calcular_atraso(self):
        return self.retrato_horario.calcular_atraso
    

class Voo(Transporte):
    def __init__(self, origem, destino, retrato_horario, status, numero_voo):
        super().__init__(origem, destino, retrato_horario, status)

        self.numero_voo = numero_voo

class Onibus(Transporte):
    def __init__(self, origem, destino, retrato_horario, status, linha_onibus):
        super().__init__(origem, destino, retrato_horario, status)

        self.linha_onibus = linha_onibus

class Trem(Transporte):
    def __init__(self, origem, destino, retrato_horario, status, linha_trem, status_operadora):
        super().__init__(origem, destino, retrato_horario, status)
        self.linha_trem = linha_trem
        self.status_operadora = status_operadora

    def calcular_atraso(self):
    #esse status vem direto da api/da operadora ent nn depende da diferença de horario
        return self.status_operadora
    
    def exibir_status(self):
        return f"Trem da linha {self.linha_trem} ({self.origem} -> {self.destino}): {self.status_operadora}"
    
