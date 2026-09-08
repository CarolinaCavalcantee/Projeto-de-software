from modelos.retrato_horario import Retrato_horario
from modelos.transporte import Voo as VooDominio, Onibus as OnibusDominio, Trem as TremDominio

def montar_voo_dominio(voo_api, horario_programado_str: str) -> VooDominio: #essa função converte os daddos brutos da api em objeto de dominio
    retrato = Retrato_horario(
        horario_programado_str, voo_api.horario_estimado.strftime("%H:%M"))#vai passar primeiro o horario programado (em texto) e dps formata p padrao

    return VooDominio(voo_api.origem, voo_api.destino, retrato, voo_api.codigo)

def montar_onibus_dominio (onibus_api, horario_programado_str: str) -> OnibusDominio:
    retrato = Retrato_horario(
        horario_programado_str, onibus_api.horario_chegada.strftime("%H:%M"))
    return OnibusDominio (onibus_api.origem, onibus_api.destino, retrato, onibus_api.linha)

def montar_trem_dominio (trem_api, horario_programado_str: str, status_operadora: str) -> TremDominio:
    retrato = Retrato_horario(
        horario_programado_str, trem_api.horario_chegada.strftime("%H:%M"))
    return TremDominio (trem_api.origem, trem_api.destino, retrato, trem_api.linha, status_operadora)
    
