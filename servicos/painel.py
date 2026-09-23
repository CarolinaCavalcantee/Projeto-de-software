import logging
def montar_painel_completo():
    dados_painel = {
        "voos": {},
        "onibus_e_trens": {},
        "avisos": []
    }

    try:
        voo = buscar_voo()
        if voo:
            dados_painel["voos"][voo.numero_voo] = voo.exibir_status()

    except Exception as e:
        logging.error(f"Erro ao buscar voo: {e}")
        dados_painel["avisos"].append("Dados temporariamente indisponíveis.")

    try:
        dados_gtfs = buscar_gtfs_api()
        transportes = processar_dados_gtfs(dados_gtfs)

        for transporte in transportes:
            if hasattr(transporte, 'trip_id'):
                id_unico = transporte.trip_id
            elif hasattr(transporte, 'linha_onibus'):
                id_unico = transporte.linha_onibus
            else:
                id_unico = transporte.linha_trem

            dados_painel["onibus_e_trens"][id_unico] = transporte.exibir_status()

    except Exception as e:
        logging.error(f"Erro ao buscar ônibus/trem: {e}")
        dados_painel["avisos"].append("Dados temporariamente indisponíveis.")

    return dados_painel
