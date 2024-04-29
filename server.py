import socket
import datetime
import struct
import random
import config

mensagens_motivacionais = [
    "Você é capaz de grandes coisas!",
    "O esforço de hoje é a recompensa de amanhã.",
    "Continue perseverando!"
]

contador_respostas = 0

def run_server():
    global contador_respostas
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 50000))  # 0.0.0.0 para aceitar conexões de qualquer IP

    print("Servidor iniciado. Aguardando mensagens...")
    try:
        while True:
            data, addr = server_socket.recvfrom(1024)
            contador_respostas += 1  # Incrementa o contador de respostas
            print(f"Mensagem recebida de {addr}")

            req_res_tipo, identificador = struct.unpack('!BH', data[:3])
            tipo = req_res_tipo & 0x0F  # Extrai os 4 bits inferiores para o tipo

            # Verifica o tipo de requisição e gera a resposta apropriada
            if tipo == config.FORMATO_DATA_HORA:
                resposta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode()
            elif tipo == config.FORMATO_MENSAGEM_MOTIVACIONAL:
                resposta = random.choice(mensagens_motivacionais).encode()
            elif tipo == config.FORMATO_CONTADOR_RESPOSTAS:
                resposta = f"O servidor enviou {contador_respostas} respostas até agora.".encode()
            elif tipo == config.FORMATO_REQUISICAO_INVALIDA:
                resposta = b"Requisicao invalida."

            # Empacota a resposta no formato especificado
            tamanho_resposta = len(resposta)
            header_resposta = struct.pack('!BHB', (1 << 4) | tipo, identificador, tamanho_resposta)
            mensagem_completa = header_resposta + resposta

            # Envia a resposta para o cliente
            server_socket.sendto(mensagem_completa, addr)
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_server()