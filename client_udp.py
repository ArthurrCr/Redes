import socket
from common import create_message, parse_response
import config

def get_user_choice():
    """Obtém a escolha do usuário do menu de opções."""
    print("\nOpções:")
    print("1: Solicitar data e hora atual")
    print("2: Solicitar uma mensagem motivacional")
    print("3: Solicitar a quantidade de respostas emitidas pelo servidor")
    print("4: Sair")
    choice = input("Escolha uma opção (1-4): ")
    return choice

def main():
    """Função principal que executa o cliente UDP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock: # Cria um socket UDP
        sock.settimeout(10)  # Configura um timeout para a resposta do servidor
        while True:
            choice = get_user_choice() # Obtém a escolha do usuário
            if choice == '4': # Se a escolha for 4, encerra o cliente
                print("Encerrando cliente...") # Exibe uma mensagem de encerramento
                break
            
            # Cria uma mensagem com base na escolha do usuário
            message = create_message(choice)
            if message is None:
                print("Opção inválida. Tente novamente.")
                continue
            
            try:
                # Envia a mensagem ao servidor
                sock.sendto(message, (config.SERVER_IP, config.SERVER_PORT))
                # Aguarda a resposta do servidor
                data, _ = sock.recvfrom(1024)
                response = parse_response(data)
                print("Resposta do servidor:", response)
            except socket.timeout:
                print("A resposta do servidor demorou demais. Tente novamente.")
            except Exception as e:
                print(f"Erro durante a comunicação: {e}")

if __name__ == "__main__":
    main()
