import struct
import random

def create_message(user_choice):
    """Cria uma mensagem de requisição baseada na escolha do usuário."""
    type_mapping = {'1': 0x00, '2': 0x01, '3': 0x02}
    req_type = type_mapping.get(user_choice)
    if req_type is None:
        return None

    # Geração aleatória de identificador entre 1 e 65535
    identifier = random.randint(1, 65535)
    # Empacota a requisição como 0 (bits 0000) para uma requisição, tipo de requisição e identificador
    message = struct.pack('!BBH', 0x00, req_type, identifier)
    return message

def parse_response(data):
    """Interpreta a resposta do servidor."""
    if not data:
        return "Nenhuma resposta recebida."
    
    # Descompacta o cabeçalho da resposta
    header = data[:4]
    res_type, identifier, size = struct.unpack('!BBH', header)
    
    # A resposta real começa após o cabeçalho, portanto, verifique se os dados recebidos são suficientes
    if len(data) != 4 + size:
        return "Dados de resposta incompletos."
    
    # Interpreta os bytes da resposta baseado no tipo
    if res_type == 0x10:  # Data e hora
        response = data[4:].decode('utf-8')
    elif res_type == 0x11:  # Mensagem motivacional
        response = data[4:].decode('utf-8')
    elif res_type == 0x12:  # Quantidade de respostas
        response = struct.unpack('!I', data[4:4+size])[0]
    else:
        return "Resposta inválida ou desconhecida."
    
    return response
