import socket
import struct
import random
import config

# Função para construir a mensagem de requisição conforme o protocolo
def construir_requisicao(tipo):
    req_res_tipo = (0 << 4) | tipo  # 0 para requisição, tipo em 4 bits inferiores
    identificador = random.randint(1, 65535)
    return req_res_tipo, identificador

# Função para construir o cabeçalho UDP
def construir_cabecalho_udp(porta_origem, porta_destino, tamanho_payload):
    tamanho_udp = 8 + tamanho_payload
    checksum_udp = 0  # Checksum pode ser zero se não calculado
    return struct.pack('!HHHH', porta_origem, porta_destino, tamanho_udp, checksum_udp)

# Função para construir o cabeçalho IP
def construir_cabecalho_ip(origem, destino, tamanho_payload):
    versao_e_ihl = (4 << 4) | 5 # 4 para IPv4, 5 para IHL (Internet Header Length) de 5 palavras de 32 bits
    tipo_servico = 0 # Tipo de serviço (DSCP + ECN), 0 para padrão
    tamanho_total = 20 + tamanho_payload # Tamanho total do datagrama em bytes
    identificacao = random.randint(0, 65535) # Identificação do datagrama
    flags_e_fragment_offset = 0 # Flags e offset de fragmentação
    ttl = 64 # Tempo de vida do pacote
    protocolo = 17  # UDP
    checksum_cabecalho = 0 # Checksum do cabeçalho, pode ser zero se não calculado
    cabecalho_ip_sem_checksum = struct.pack('!BBHHHBBH4s4s', versao_e_ihl, tipo_servico, tamanho_total, identificacao,
                                            flags_e_fragment_offset, ttl, protocolo, checksum_cabecalho,
                                            socket.inet_aton(origem), socket.inet_aton(destino))
    checksum_cabecalho = calcular_checksum(cabecalho_ip_sem_checksum)
    return struct.pack('!BBHHHBBH4s4s', versao_e_ihl, tipo_servico, tamanho_total, identificacao,
                       flags_e_fragment_offset, ttl, protocolo, checksum_cabecalho,
                       socket.inet_aton(origem), socket.inet_aton(destino))

def calcular_checksum(source_string):
    sum = 0
    count = 0
    while count < len(source_string):
        val = source_string[count + 1] * 256 + source_string[count] # Ordem da rede
        sum = sum + val 
        sum = sum & 0xffffffff # Se um carry ocorrer, ele é adicionado ao final
        count += 2 # Pula 2 bytes
    sum = (sum >> 16) + (sum & 0xffff) # Desloca 16 bits e soma novamente
    sum += (sum >> 16) # Soma o carry
    answer = ~sum & 0xffff # Bitwise NOT e 16 bits
    return answer

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

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

        req_res_tipo, identificador = construir_requisicao(opcao)
        mensagem = struct.pack('!BHB', req_res_tipo, identificador, 0)  # 0 no tamanho da resposta porque é uma requisição

        # Construir cabeçalhos
        udp_header = construir_cabecalho_udp(config.CLIENT_PORT, config.SERVER_PORT, len(mensagem))
        ip_header = construir_cabecalho_ip(config.CLIENT_IP, config.SERVER_IP, len(udp_header) + len(mensagem))

        # Pacote completo
        pacote = ip_header + udp_header + mensagem

        # Enviar pacote
        sock.sendto(pacote, (config.SERVER_IP, 0))
        print("Mensagem enviada.")

finally:
    sock.close()
    print('Socket fechado')
