import socket
import struct
import config
import random

def construir_requisicao(tipo):
    req_res_tipo = (0 << 4) | tipo  # 0 para req, tipo nos 4 bits inferiores
    identificador = random.randint(1, 65535)  # Identificador de 16 bits
    mensagem_bytes = struct.pack('!BH', req_res_tipo, identificador)  # Empacota os dados
    return mensagem_bytes, identificador

def construir_cabecalho_udp(orig_porta, dest_porta, dados):
    comprimento = 8 + len(dados)  # 8 bytes de cabeçalho UDP + tamanho dos dados
    checksum = 0  # Para fins de simplicidade, deixamos o checksum como zero
    cabecalho = struct.pack('!HHHH', orig_porta, dest_porta, comprimento, checksum)
    return cabecalho + dados

def interpretar_resposta(resposta_bytes):
    # Pula os cabeçalhos IP (20 bytes) e UDP (8 bytes)
    udp_header_length = 8
    resposta_bytes = resposta_bytes[28:]
    
    if len(resposta_bytes) < 6:
        return "Resposta do servidor incompleta."
    
    req_res_tipo, identificador = struct.unpack('!BH', resposta_bytes[:3])
    req_res = req_res_tipo >> 4  # Extrai os 4 bits superiores para req/res
    tipo = req_res_tipo & 0x0F   # Extrai os 4 bits inferiores para o tipo
    tamanho_resposta = resposta_bytes[3]  # O 4º byte é o tamanho da resposta

    if req_res != 1:  # Verifica se a mensagem é uma resposta
        return "Mensagem recebida não é uma resposta."

    if len(resposta_bytes) < 4 + tamanho_resposta:
        return f"Tamanho da resposta ({tamanho_resposta} bytes) não corresponde ao esperado ({len(resposta_bytes) - 4} bytes)."

    resposta = resposta_bytes[4:4+tamanho_resposta]

    if tipo == config.FORMATO_REQUISICAO_INVALIDA and tamanho_resposta == 0:
        return f"Requisição inválida ou problema no identificador {identificador}."
    
    elif tipo == config.FORMATO_CONTADOR_RESPOSTAS:
        if tamanho_resposta != 4:
            return "Formato da resposta do contador de respostas é incorreto."
        contador_respostas, = struct.unpack('!I', resposta)
        return contador_respostas
    else:
        return resposta.decode('utf-8', errors='ignore')

# Configurações
destino_ip = config.SERVER_IP
orig_porta = config.CLIENT_PORT
dest_porta = config.SERVER_PORT

# Criar um socket RAW para UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

try:
    while True:
        print("\nMenu de Opções:")
        print("0 - Data e hora atual")
        print("1 - Mensagem motivacional")
        print("2 - Quantidade de respostas do servidor")
        print("3 - Sair")
        opcao = int(input("Escolha uma opção: "))

        if opcao == 3:
            print("Saindo...")
            break

        # Construir a mensagem de requisição e enviar para o servidor
        mensagem, identificador = construir_requisicao(opcao)
        pacote_udp = construir_cabecalho_udp(orig_porta, dest_porta, mensagem)
        sock.sendto(pacote_udp, (destino_ip, dest_porta))

        # Receber a resposta do servidor
        data, _ = sock.recvfrom(1024)
        print(f"Tamanho dos dados recebidos: {len(data)}")
        try:
            resposta = interpretar_resposta(data)  # Ignora o cabeçalho UDP de 8 bytes na resposta
            print(f"Resposta do servidor para o identificador {identificador}: {resposta}")
        except struct.error as e:
            print(f"Erro ao interpretar resposta: {e}")

finally:
    sock.close()
    print('Socket fechado')
