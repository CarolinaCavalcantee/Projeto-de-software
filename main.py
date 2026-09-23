from modelos.registro_transportes import RegistroTransportes
import requests
import logging 
logging.basicConfig(level = logging.WARNING, format="[AVISO]%(message)s")
from servicos.aviationstack_usuario import AviationStack
from servicos.gtfs_usuario import GtfsUsuario
from api_oculta import AviationStackService, GtfsService
from servicos.montador import montar_voo_dominio, montar_onibus_dominio
from modelos.historico_retratos import HistoricoRetratos
from modelos.viagem import Viagem
from modelos.registro_transportes import RegistroTransportes #rf9
from modelos.canal_notificacao import CanalEmail, CanalPush  # rf10
from modelos.usuario import UsuarioInscrito
from servicos.notificador import Notificador

historico = HistoricoRetratos()
painel = RegistroTransportes() #rf9 p reconhecer transportes repetidos
notificador = Notificador() #rf10 p usuario se inscrever




def buscar_voo():
    try:
        cliente_voo = AviationStack()
        json_voo = cliente_voo.buscar_voo("SQ8451")  

        horario_partida = json_voo.get("departure", {})
        if not horario_partida.get("estimated") and not horario_partida.get("scheduled"):
            logging.warning(f"Voo {json_voo.get('flight', {}).get('iata', '?')}: sem horário programado nem estimado")
            return None
    
        voo_api = AviationStackService.criar_voo_json(json_voo)
        voo_dominio = montar_voo_dominio(voo_api, "03:00")  # ajusta pro horario programado real

        voo_dominio.id_transporte = voo_api.codigo
        historico.registrar(voo_dominio.id_transporte, voo_dominio.retrato_horario)

        return voo_dominio
    except (requests.RequestException, ValueError, KeyError) as erro:
        print(f"Não foi possível buscar o voo: {erro}")
        return None


def buscar_onibus():
    try:
        cliente_onibus = GtfsUsuario(
            "http://realtime4.mobilibus.com/web/4ch6j/trip-updates?accesskey=982a57efd77a9462bf1665696fb25984"
        )
        atualizacoes = cliente_onibus.buscar_atualizacoes()

        atualizacao_valida = None
        for a in atualizacoes:
            paradas = a["trip_update"]["stop_time_update"]
            if not paradas or not paradas[0].get("departure") or not (paradas[-1].get("arrival") or paradas[-1].get("departure")):
                trip_id = a.get("trip_update", {}).get("trip", {}).get("trip_id", "desconhecido")
                logging.warning(f"Atualização de ônibus {trip_id} : horário incompleto")
                continue

            atualizacao_valida = a
            break 

        if not atualizacao_valida:
            print("Nenhuma atualização de ônibus encontrada.")
            return None

        onibus_api = GtfsService.criar_onibus_gtfs(atualizacao_valida)
        onibus_dominio = montar_onibus_dominio(onibus_api, "21:00") #ajusta pro horario programado real

        onibus_dominio.id_transporte = onibus_api.identificador  
        historico.registrar(onibus_dominio.id_transporte, onibus_dominio.retrato_horario)

        return onibus_dominio
    except (requests.RequestException, ValueError, KeyError) as erro:
        print(f"Não foi possível buscar o ônibus: {erro}")
        return None

def cadastrar_usuario() -> UsuarioInscrito:
    print("\n---Cadastro para notificar atrasos ---\n")

    nome = input("Digite seu nome: ").strip()
    while not nome:
        nome = input("O nome não pode ficar vazio. Digite seu nome:").strip()

    inscricoes = []

    print("Canais disponíveis:")
    print("  1 - E-mail")
    print("  2 - Push")
    print("  3 - E-mail e Push")
    escolha = input("Escolha o(s) canal(is) [1/2/3]: ").strip()
    while escolha not in ("1", "2", "3"):
        escolha = input("Opção inválida. Digite 1, 2 ou 3: ").strip()

    if escolha in ("1", "3"):
        email = input("Digite seu e-mail: ").strip()
        while not email or "@" not in email:
            email = input("E-mail inválido, precisa ter '@'. Digite de novo: ").strip()

        inscricoes.append((CanalEmail(), email))

    if escolha in ("2", "3"):
        telefone = input("Seu telefone: ").strip()
        while not telefone:
            telefone = input("Telefone não pode ficar vazio: ").strip()

        inscricoes.append((CanalPush(), telefone))

    return UsuarioInscrito(nome, inscricoes)

def registrar_no_painel(transporte, nome: str):
    #rf9 p registrar o transporte no painel e avisar se for uma busca duplicada
    if transporte is None:
        return
    novo = painel.registrar(transporte)
    if novo:
        print(f"{nome} adicionado ao painel.")
    else:
        print(f"{nome} já estava no painel (busca repetida reconhecida como o mesmo transporte).")
    notificador.notificar_atraso(transporte)  #rf10 avisa se tiver atraso

def exibir_menu():
    print("\n Painel de status de transportes")
    print("1 - Ver status do voo;")
    print("2 - Ver status do ônibus;")
    print("3 - Ver painel completo (voo + ônibus);")
    print("4 - Ver viagem com múltiplos trechos (voo + ônibus);")
    print("5 - Buscar de novo e comparar;")
    print("6 - Sair")


def main():
    usuario = cadastrar_usuario()
    notificador.inscrever(usuario)
    canais_nomes = ", ".join(type(c).__name__.replace("Canal", "") for c, _ in usuario.inscricoes)
    print(f"\n{usuario.nome} inscrito para receber notificações por: {canais_nomes}\n")
 
    voo = buscar_voo()
    registrar_no_painel(voo, "Voo")
    onibus = buscar_onibus()
    registrar_no_painel(onibus, "Ônibus")
 
    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ")
 
        if escolha == "1":
            if voo:
                print(voo.exibir_status())
            else:
                print("Sem dados de voo disponível.")
 
        elif escolha == "2":
            if onibus:
                print(onibus.exibir_status())
            else:
                print("Sem dado de ônibus disponível.")
 
        elif escolha == "3":
            transportes = painel.listar()  # RF9: painel já deduplicado
            if not transportes:
                print("Nenhum transporte disponível.")
            else:
                print(f"({painel.quantidade()} transporte(s) único(s) no painel)")
                for t in transportes:
                    print(t.exibir_status())
 
        elif escolha == "4":
            if voo and onibus:
                viagem = Viagem([voo, onibus])
                print(viagem.exibir_status())
            else:
                print("Preciso do voo E do ônibus disponíveis para montar a viagem.")
 
        elif escolha == "5":
            print("Buscando dados novos...")
            voo = buscar_voo()
            registrar_no_painel(voo, "Voo")  # RF9: se for o mesmo voo, não duplica
            onibus = buscar_onibus()
            registrar_no_painel(onibus, "Ônibus")
 
            if voo:
                print("Voo:", historico.mudou(voo.id_transporte))
            if onibus:
                print("Ônibus:", historico.mudou(onibus.id_transporte))
 
        elif escolha == "6":
            print("Finalizando.")
            break
 
        else:
            print("Opção inválida.")
 
 
if __name__ == "__main__":
    main()