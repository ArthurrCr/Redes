import socket
import config
import struct
import os

# Verifica se é root
if not os.geteuid() == 0:
    exit("Este script precisa ser rodado como root.")

# Cria um socket RAW
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

# Informa ao kernel que está fornecendo os cabeçalhos IP
sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

try:
    while True:
        print("\nMenu de Opções:")
        print("1 - Data e hora atual")
        print("2 - Mensagem motivacional")
        print("3 - Quantidade de respostas do servidor")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '4':
            print("Saindo...")
            break

        # Empacotar os dados da opção em uma estrutura adequada para envio
        # Como exemplo, vamos enviar apenas a opção escolhida em formato de string
        # Uma implementação completa exigiria a construção manual do cabeçalho IP e UDP
        message = opcao.encode()

        # Envio de uma mensagem fictícia, uma implementação real precisaria dos cabeçalhos corretos
        # Isso é apenas ilustrativo, o envio real de pacotes RAW é mais complexo
        sock.sendto(message, (config.SERVER_IP, config.SERVER_PORT))

        # Como estamos utilizando socket RAW, não podemos utilizar a função recvfrom diretamente
        # para obter a resposta, pois ela incluiria cabeçalhos que não desejamos.
        # Em um uso real, você precisaria implementar uma escuta em loop para pacotes recebidos
        # e filtrar pela resposta esperada com os cabeçalhos IP e UDP corretos.
        
        # Este é apenas um exemplo ilustrativo e não funcionará como está.
        # data, _ = sock.recvfrom(65535)
        # print("Resposta do servidor:", data)

finally:
    print('Fechando o socket')
    sock.close()
