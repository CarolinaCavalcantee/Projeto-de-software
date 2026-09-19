class Transporte:
    def __init__(self, origem, destino, retrato_horario):
        self.origem = origem
        self.destino = destino
        self.retrato_horario = retrato_horario

    def calcular_diferenca(self):
        return self.retrato_horario.calcular_diferenca()
        #vms calcular a diferenca de tempo o objeto de horario

    def calcular_atraso(self):
        raise NotImplementedError #se a subclasse nn implementar, dá erro

    def exibir_status(self):
        raise NotImplementedError

    #RF9-duplicação de buscas usando polimorfismo
    def identificador_unico(self):
        raise NotImplementedError   

    def chave_identificacao(self) -> str:
        return f"{type(self).__name__}:{self.identificador_unico()}"

class Voo(Transporte):
    def __init__(self, origem, destino, retrato_horario, numero_voo):
        super().__init__(origem, destino, retrato_horario)
        self.numero_voo = numero_voo

    def calcular_atraso(self):
        diferenca = self.calcular_diferenca()
        if diferenca <= 15:
            return 0 
        else:
            return diferenca #tolerancia de 15min

    def exibir_status(self):
        atraso = self.calcular_atraso()
        horario = self.retrato_horario.horario_real.strftime("%H:%M")
        if atraso == 0:
            status = "No horário"  
        else:
            status = f"Atrasado em {int(atraso)} minutos"
        return f"Voo {self.numero_voo} -> {horario} {status}"

    def identificador_unico(self):
        return self.numero_voo   

class Onibus(Transporte):
    def __init__(self, origem, destino, retrato_horario, linha_onibus, identificador=None):
        super().__init__(origem, destino, retrato_horario)
        self.linha_onibus = linha_onibus
        if identificador is not None:
            self.identificador = identificador  
        else:
            self.identificador = linha_onibus

    def calcular_atraso(self):
        diferenca = self.calcular_diferenca()
        if diferenca <= 10:
            return 0 
        else:
            return diferenca

    def exibir_status(self):
        atraso = self.calcular_atraso()
        horario = self.retrato_horario.horario_real.strftime("%H:%M")
        if atraso == 0:
            status = "No horário"
        else:
            status = f"Atrasado em {int(atraso)} minutos"
        return f"Ônibus {self.linha_onibus} -> {horario} {status}"

    def identificador_unico(self):
        return self.identificador 

class Trem(Transporte):
    def __init__(self, origem, destino, retrato_horario, linha_trem, status_operadora, identificador=None):
        super().__init__(origem, destino, retrato_horario)
        self.linha_trem = linha_trem
        self.status_operadora = status_operadora
        if identificador is not None:
            self.identificador = identificador 
        else:
            self.identificador = linha_trem

    def calcular_atraso(self):
        return 0 if self.status_operadora == "no horário" else 1

    def exibir_status(self):
        return f"Trem {self.linha_trem} -> {self.origem} → {self.destino}: {self.status_operadora}"

    def identificador_unico(self):
        return self.identificador