# aqui a gnt vai fzr um formato que, sem as apis falharem, a gnt tem alguma coisa ainda
def montar_painel_completo():
    dados_painel = {
        "voos": [],
        "onibus_e_trens": [],
        "avisos": []
    }

    #primeiro vms tentar achar cada api separada
    try:
        voo = buscar_voo()
        if voo:
            dados_painel["voos"].append(voo.exibir_status())
    except Exception as e:
        print(f"Erro ao carregar voo {e}")
        dados_painel["avisos"].append("Dados de voos temporariamente indisponíveis.")

    try:
        dados_gtfs = buscar_gtfs_api()
        transportes = processar_dados_gtfs(dados_gtfs)
        for transporte in transportes:
            dados_painel["onibus_e_trens"].append(transporte.exibir_status())
            
    except Exception as e:
        print(f"Erro ao carregar ônibus/trem {e}")
        dados_painel["avisos"].append("Dados de transportes terrestres temporariamente indisponíveis.")

    return dados_painel
