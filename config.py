# IP do servidor ao qual os clientes irão se conectar
SERVER_IP = '15.228.191.109'

# Porta do servidor para as conexões dos clientes
SERVER_PORT = 50000

# IP do cliente (necessário para o cabeçalho IP em client_raw.py)
SOURCE_IP = '192.168.1.100' 

# Porta de origem para uso no cliente RAW
SOURCE_PORT = 12345

# Formatos de mensagem pré-definidos
FORMATO_DATA_HORA = 0b0000  # 0000 para data e hora
FORMATO_MENSAGEM_MOTIVACIONAL = 0b0001  # 0001 para mensagem motivacional
FORMATO_CONTADOR_RESPOSTAS = 0b0010  # 0010 para contador de respostas
FORMATO_REQUISICAO_INVALIDA = 0b0011  # 0011 para requisição inválida   
