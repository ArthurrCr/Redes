import socket
import config

# Função para formatar a mensagem para o servidor
def formatar_requisicao(opcao):
    # Aqui você deve implementar a lógica para criar uma mensagem
    # que esteja de acordo com o protocolo especificado pelo servidor.
    # Este é um exemplo genérico:
    if opcao == '1':
        return 'GET TIME'
    elif opcao == '2':
        return 'GET MOTIVATION'
    elif opcao == '3':
        return 'GET COUNT'
    # Adicione mais condições conforme necessário para outros tipos de mensagens.
    else:
        return 'UNKNOWN COMMAND'

# Criar um socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        print("\nMenu de Opções:")
        print("1 - Data e hora atual")
        print("2 - Mensagem motivacional")
        print("3 - Quantidade de respostas do servidor")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        # Formatar a requisição
        mensagem_formatada = formatar_requisicao(opcao)
        sock.sendto(mensagem_formatada.encode(), (config.SERVER_IP, config.SERVER_PORT))

        if opcao == '4':
            print("Saindo...")
            break

        # Receber a resposta do servidor
        data, _ = sock.recvfrom(4096)
        resposta = data.decode()

        # Aqui você deve implementar a lógica para converter a resposta do servidor
        # para um formato legível, assumindo que ela pode não vir legível.
        # O exemplo abaixo simplesmente assume que a resposta já é legível.
        print("Resposta do servidor:", resposta)

finally:
    sock.close()
