# Arthur César Cardoso Clemente - 20190175757
# Ruy de Morais e Silva - 2019017695
# Deivison Rodrigues Jordão - 20200023728
import socket
import struct
import config
import random

def construir_requisicao(tipo):
    # req_res_tipo combina 4 bits para req/res e 4 bits para tipo
    req_res_tipo = (0 << 4) | tipo  # 0 para requisição (req), tipo nos 4 bits inferiores
    
    # identificador é um valor aleatório de 16 bits para identificar a requisição
    identificador = random.randint(1, 65535)
    
    # Empacota os valores em uma estrutura de bytes
    # Formato '!BH' especifica:
    # - '!': big-endian (byte order de rede)
    # - 'B': unsigned char (1 byte)
    # - 'H': unsigned short (2 bytes)
    # 0 é adicionado para o tamanho da resposta (1 byte, mas não usado)
    return struct.pack('!BHB', req_res_tipo, identificador, 0), identificador

def interpretar_resposta(resposta_bytes):
    
    # Desempacota o cabeçalho da resposta
    # Formato '!BH' especifica:
    # - '!': big-endian (byte order de rede)
    # - 'B': unsigned char (1 byte)
    # - 'H': unsigned short (2 bytes)
    req_res_tipo, identificador = struct.unpack('!BH', resposta_bytes[:3]) # Extrai os 3 primeiros bytes
    
    # Extrai os 4 bits inferiores para o tipo de resposta
    tipo = req_res_tipo & 0x0F 
    
    # O 4º byte é o tamanho da resposta
    tamanho_resposta = resposta_bytes[3]
    
    # Extrai os bytes da resposta propriamente dita
    resposta = resposta_bytes[4:4 + tamanho_resposta]

    # Verifica se a resposta indica uma requisição inválida
    if tipo == config.FORMATO_REQUISICAO_INVALIDA and tamanho_resposta == 0:
        identificador = 0
        return f"Requisição inválida {identificador}."
    
    # Verifica se a resposta é o contador de respostas
    elif tipo == config.FORMATO_CONTADOR_RESPOSTAS:

        # Desempacota os 4 bytes da resposta como um inteiro sem sinal
        contador_respostas, = struct.unpack('!I', resposta_bytes[4:8])
        return contador_respostas

    # Caso contrário, trata a resposta como uma string
    else:
        return resposta.decode('utf-8', errors='ignore')  # Decodifica a resposta para string


# Criar um socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

        # Envia a mensagem para o servidor
        sock.sendto(mensagem, (config.SERVER_IP, config.SERVER_PORT))

        # Recebe a resposta do servidor
        data, _ = sock.recvfrom(255) # Recebe até 255 bytes
        print(f"Tamanho dos dados recebidos: {len(data)}")
    
        # Interpretar a resposta do servidor
        resposta = interpretar_resposta(data)
        print(f"Resposta do servidor para o identificador {identificador}: {resposta}")
        
finally:
    sock.close()
    print('Socket fechado')
