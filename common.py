import struct

def create_message(user_choice):
    """Cria uma mensagem de requisição baseada na escolha do usuário."""
    if user_choice == '1':
        req_type = 0x00  # Data e hora
    elif user_choice == '2':
        req_type = 0x01  # Mensagem motivacional
    elif user_choice == '3':
        req_type = 0x02  # Quantidade de respostas
    else:
        return None

    identifier = 14161  # Exemplo de identificador, você pode implementar algo para gerar aleatoriamente
    message = struct.pack('!BBH', 0x00, req_type, identifier)
    return message

def parse_response(data):
    """Interpreta a resposta do servidor."""
    if not data:
        return "Nenhuma resposta recebida."
    
    # Descompacta o cabeçalho da resposta
    res_type, identifier, size = struct.unpack('!BBH', data[:4])
    # Verifica o tipo de resposta
    if res_type == 0x10:  # Data e hora
        format_str = '!{}s'.format(size)
        response = struct.unpack(format_str, data[4:4+size])[0].decode()
    elif res_type == 0x11:  # Mensagem motivacional
        format_str = '!{}s'.format(size)
        response = struct.unpack(format_str, data[4:4+size])[0].decode()
    elif res_type == 0x12:  # Quantidade de respostas
        response = struct.unpack('!I', data[4:4+size])[0]
    else:
        return "Resposta inválida ou desconhecida."
    
    return response
