import socket
import struct
from common import create_message, parse_response
import config

def checksum(data):
    """Calcula o checksum Internet (RFC 1071)."""
    s = 0
    n = len(data) % 2
    for i in range(0, len(data)-n, 2):
        s += (data[i] << 8) + (data[i+1])
    if n:
        s += (data[-1] << 8)
    while (s >> 16):
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xffff
    return s

def create_udp_header(src_port, dest_port, length, payload):
    """Cria um cabeçalho UDP."""
    pseudo_header = struct.pack('!4s4sBBH',
                                socket.inet_aton(config.SOURCE_IP),  # IP origem
                                socket.inet_aton(config.SERVER_IP),  # IP destino
                                0,  # Zerado
                                socket.IPPROTO_UDP,
                                length + 8)  # Comprimento do cabeçalho + dados
    udp_header = struct.pack('!HHHH',
                             src_port,  # Porta origem
                             dest_port,  # Porta destino
                             length + 8,  # Comprimento UDP
                             0)  # Checksum (inicialmente zero)
    checksum_val = checksum(pseudo_header + udp_header + payload)
    udp_header = struct.pack('!HHHH', src_port, dest_port, length + 8, checksum_val)
    return udp_header

def create_ip_header(length):
    """Cria um cabeçalho IP básico para um datagrama IP."""
    version = 4
    ihl = 5  # Internet Header Length
    type_of_service = 0
    total_length = 20 + length  # IP header length + UDP header length + data length
    packet_id = 54321  # Identificador do pacote
    fragment_offset = 0
    ttl = 255
    protocol = socket.IPPROTO_UDP
    header_checksum = 0  # O checksum será calculado depois
    source_ip = socket.inet_aton(config.SOURCE_IP)
    dest_ip = socket.inet_aton(config.SERVER_IP)

    ip_header = struct.pack('!BBHHHBBH4s4s',
                            (version << 4) + ihl, type_of_service, total_length,
                            packet_id, fragment_offset, ttl, protocol,
                            header_checksum, source_ip, dest_ip)

    header_checksum = checksum(ip_header)
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            (version << 4) + ihl, type_of_service, total_length,
                            packet_id, fragment_offset, ttl, protocol,
                            header_checksum, source_ip, dest_ip)
    return ip_header

def main():
    """Função principal que executa o cliente RAW."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except socket.error as msg:
        print('Socket could not be created. Error Code:', str(msg[0]), 'Message', msg[1])
        return

    while True:
        message = create_message('1')  # Exemplo com opção fixa
        udp_header = create_udp_header(config.SOURCE_PORT, config.SERVER_PORT, len(message), message)
        ip_header = create_ip_header(len(udp_header) + len(message))
        packet = ip_header + udp_header + message

        try:
            s.sendto(packet, (config.SERVER_IP, 0))
            # O recebimento de respostas em sockets RAW é complexo e requer processamento adicional.
        except Exception as e:
            print(f"Erro ao enviar pacote: {e}")

if __name__ == "__main__":
    main()
