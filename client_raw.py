import socket
import struct
import config
import random


def construir_requisicao(tipo):
    # `req_res_tipo` representa o tipo da mensagem, armazenando `req/res` no nibble mais significativo e o `tipo` nos bits menos significativos
    req_res_tipo = (0 << 4) | tipo
    
    # `identificador` é um número aleatório de 16 bits para identificar a requisição
    identificador = random.randint(1, 65535)
    
    # A mensagem é empacotada com `!BHB` (1 byte para `req_res_tipo`, 2 bytes para `identificador`, e 1 byte vazio)
    return struct.pack('!BHB', req_res_tipo, identificador, 0), identificador


def calcular_checksum(source_string):
    # Adiciona um byte de preenchimento se o comprimento da string de origem for ímpar
    if len(source_string) % 2 == 1:
        source_string += b'\0'
    
    # Soma todos os valores de 16 bits extraídos da string
    sum_result = sum(struct.unpack('!%dH' % (len(source_string) // 2), source_string))
    
    # Faz a soma usando apenas os 16 bits menos significativos
    sum_result = (sum_result & 0xffff) + (sum_result >> 16)
    
    # Retorna o complemento de 1 da soma
    return ~sum_result # ~ é o operador de complemento de bits


def construir_cabecalho_udp(orig_porta, dest_porta, dados, ip_origem, ip_destino):
    # Comprimento total do pacote UDP (8 bytes de cabeçalho + dados)
    comprimento = 8 + len(dados)
    
    # Pseudo-cabeçalho IP usado no cálculo do checksum, com informações IP e de protocolo
    pseudo_header = struct.pack('!4s4sBBH', socket.inet_aton(ip_origem), socket.inet_aton(ip_destino), 0, socket.IPPROTO_UDP, comprimento)
    
    # Cabeçalho UDP sem checksum
    cabecalho_udp = struct.pack('!HHHH', orig_porta, dest_porta, comprimento, 0)
    
    # Calcula o checksum usando o pseudo-cabeçalho, cabeçalho UDP e os dados
    checksum = calcular_checksum(pseudo_header + cabecalho_udp + dados) & 0xffff # & 0xffff para manter 16 bits
    
    # Empacota o cabeçalho UDP com o checksum calculado e adiciona os dados (payload)
    return struct.pack('!HHHH', orig_porta, dest_porta, comprimento, checksum) + dados


def interpretar_resposta(resposta_bytes):
    # Pula os primeiros 28 bytes (20 do cabeçalho IP e 8 do cabeçalho UDP)
    resposta_bytes = resposta_bytes[28:]
    
    # Desempacota os primeiros 3 bytes da resposta para obter `req_res_tipo` e `identificador`
    req_res_tipo, identificador = struct.unpack('!BH', resposta_bytes[:3]) 
    
    # O 4º byte é o tamanho da resposta
    tamanho_resposta = resposta_bytes[3]
    
    # Extrai o tipo da resposta (4 bits menos significativos)
    tipo = req_res_tipo & 0x0F # & 0x0F para manter os 4 bits menos significativos
    
    # Extrai a parte dos dados da resposta
    resposta = resposta_bytes[4:4+tamanho_resposta]

    # Verifica se o tipo da resposta é `FORMATO_REQUISICAO_INVALIDA`
    if tipo == config.FORMATO_REQUISICAO_INVALIDA:
        identificador = 0
        return f"Requisição inválida {identificador}."
    
    # Verifica se o tipo da resposta é `FORMATO_CONTADOR_RESPOSTAS`
    elif tipo == config.FORMATO_CONTADOR_RESPOSTAS:
        
        # Desempacota os 4 bytes da resposta como um inteiro sem sinal
        contador_respostas, = struct.unpack('!I', resposta)
        return contador_respostas
    
    # Caso contrário, trata a resposta como uma string
    else:
        return resposta.decode('utf-8', errors='ignore')


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

        # Constrói a mensagem e o identificador da requisição
        mensagem, identificador = construir_requisicao(opcao)

        # Constrói o pacote UDP com o cabeçalho e os dados
        pacote_udp = construir_cabecalho_udp(config.CLIENT_PORT, config.SERVER_PORT, mensagem, config.CLIENT_IP, config.SERVER_IP)
        
        # Envia o pacote UDP para o servidor
        sock.sendto(pacote_udp, (config.SERVER_IP, config.SERVER_PORT))

        # Recebe a resposta do servidor
        data, _ = sock.recvfrom(255)
        print(f"Tamanho dos dados recebidos: {len(data)}")

        # Interpreta a resposta do servidor
        resposta = interpretar_resposta(data)
        print(f"Resposta do servidor para o identificador {identificador}: {resposta}")

finally:
    sock.close()
    print('Socket fechado')
