import socket
import datetime

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 50000))  # Ajuste conforme necessário

    print("Servidor iniciado. Aguardando mensagens...")
    try:
        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"Mensagem recebida de {addr}")
            # Simplificação: sempre responde com a data e hora atual
            now = datetime.datetime.now()
            response = now.strftime("%Y-%m-%d %H:%M:%S").encode()
            server_socket.sendto(response, addr)
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_server()
