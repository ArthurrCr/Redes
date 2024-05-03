Aqui está um esboço para o seu `README.md`:

# Projeto Cliente/Servidor UDP

Este projeto implementa dois tipos de clientes que enviam requisições para um servidor UDP que escuta na porta 50000.

## Objetivo

Implementar clientes que se comuniquem com o servidor via UDP e socket raw, utilizando o protocolo UDP/IP, conforme especificado.

## Estrutura do Projeto

O projeto é composto por três arquivos principais:

- `server.py`: Implementa o servidor UDP, que responde a requisições.
- `client_udp.py`: Cliente tradicional usando UDP para enviar requisições ao servidor.
- `client_raw.py`: Cliente usando socket raw para enviar requisições UDP ao servidor.

## Configuração

Configure os IPs e portas no arquivo `config.py`:

```python
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
CLIENT_IP = '192.168.1.105'
CLIENT_PORT = 59155

FORMATO_DATA_HORA = 0b0000  # 0000 para data e hora
FORMATO_MENSAGEM_MOTIVACIONAL = 0b0001  # 0001 para mensagem motivacional
FORMATO_CONTADOR_RESPOSTAS = 0b0010  # 0010 para contador de respostas
FORMATO_REQUISICAO_INVALIDA = 0b0011  # 0011 para requisição inválida
```
## Como Usar

1. **Servidor**: Execute o `server.py` para iniciar o servidor.
2. **Cliente UDP**: Execute `client_udp.py` para usar o cliente UDP tradicional.
3. **Cliente Raw**: Execute `client_raw.py` para usar o cliente raw.

### Funcionalidades

- **Data e Hora Atual**: Requisição para obter a data e hora atuais.
- **Mensagem Motivacional**: Requisição para receber uma mensagem motivacional.
- **Contador de Respostas**: Requisição para contar quantas respostas o servidor enviou.

### Cálculo do Checksum

O projeto usa um cálculo de checksum para as mensagens enviadas pelo cliente raw, conforme especificado na [RFC 768](https://tools.ietf.org/html/rfc768).