import socket
import struct
import config
import random

# Função para construir a mensagem de requisição
def construir_requisicao(tipo):
    req_res_tipo = (0 << 4) | tipo  # 0 para req, tipo em 4 bits inferiores
    identificador = random.randint(1, 65535)
    # Constrói a mensagem com o formato correto
    mensagem_bytes = struct.pack('!BH', req_res_tipo, identificador)
    return mensagem_bytes, identificador

# Função para interpretar a resposta do servidor
def interpretar_resposta(resposta_bytes):
    # Verifica se os bytes recebidos estão de acordo com o cabeçalho esperado
    if len(resposta_bytes) < 6:  # Cabeçalho de 4 bytes + tamanho da resposta de 1 byte + pelo menos 1 byte de resposta
        return "Resposta do servidor incompleta."
    
    # Extrai os campos da mensagem de resposta (1 byte para req_res e tipo, 2 bytes para identificador)
    req_res_tipo, identificador = struct.unpack('!BH', resposta_bytes[:3])
    req_res = req_res_tipo >> 4  # Extrai os 4 bits superiores para req/res
    tipo = req_res_tipo & 0x0F   # Extrai os 4 bits inferiores para o tipo
    tamanho_resposta = resposta_bytes[3]  # O 4º byte é o tamanho da resposta

    if req_res != 1:  # Verifica se a mensagem é uma resposta
        return "Mensagem recebida não é uma resposta."

    if len(resposta_bytes) < 4 + tamanho_resposta:
        return f"Tamanho da resposta ({tamanho_resposta} bytes) não corresponde ao esperado ({len(resposta_bytes) - 4} bytes)."

    # O resto da mensagem é a resposta
    resposta = resposta_bytes[4:4+tamanho_resposta]

    if tipo == 0b1111 and tamanho_resposta == 0:
        return f"Requisição inválida ou problema no identificador {identificador}."
    elif tipo == config.FORMATO_CONTADOR_RESPOSTAS:
        # O tamanho da resposta deve ser exatamente 4 bytes para o contador de respostas
        if tamanho_resposta != 4:
            return "Formato da resposta do contador de respostas é incorreto."
        # Desempacota os próximos 4 bytes como um inteiro sem sinal
        contador_respostas, = struct.unpack('!I', resposta_bytes[4:8])
        return contador_respostas
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

        # Construir a mensagem de requisição e enviar para o servidor
        mensagem, identificador = construir_requisicao(opcao)
        sock.sendto(mensagem, (config.SERVER_IP, config.SERVER_PORT))

        # Receber a resposta do servidor
        data, _ = sock.recvfrom(1024)  # Tamanho do buffer definido de acordo com a especificação
        print(f"Tamanho dos dados recebidos: {len(data)}")
        try:
            resposta = interpretar_resposta(data)
            print(f"Resposta do servidor para o identificador {identificador}: {resposta}")
        except struct.error as e:
            print(f"Erro ao interpretar resposta: {e}")

finally:
    sock.close()
    print('Socket fechado')
