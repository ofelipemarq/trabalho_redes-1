import socket
from datetime import datetime


HOST = "0.0.0.0"
PORTA = 1220
BUFFER = 1024


def horario():
    return datetime.now().strftime("%H:%M:%S")


servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    servidor.bind((HOST, PORTA))

    print("=" * 55)
    print("SERVIDOR UDP")
    print("=" * 55)
    print(f"[{horario()}] Servidor iniciado.")
    print(f"[{horario()}] Aguardando datagramas na porta {PORTA}...")

    while True:
        dados, endereco_cliente = servidor.recvfrom(BUFFER)

        ip_cliente = endereco_cliente[0]
        porta_cliente = endereco_cliente[1]

        mensagem = dados.decode("utf-8")

        print("\n" + "-" * 55)
        print(f"[{horario()}] Datagrama recebido.")
        print(f"Origem: {ip_cliente}:{porta_cliente}")
        print(f"Mensagem: {mensagem}")

        if mensagem.lower() == "sair":
            resposta = "Solicitação de encerramento recebida."

            servidor.sendto(
                resposta.encode("utf-8"),
                endereco_cliente
            )

            print(
                f"[{horario()}] "
                f"Cliente {ip_cliente}:{porta_cliente} encerrou a sessão."
            )

            # O servidor NÃO encerra.
            continue

        resposta = "Datagrama recebido com sucesso!"

        servidor.sendto(
            resposta.encode("utf-8"),
            endereco_cliente
        )

        print(
            f"[{horario()}] "
            "Resposta enviada ao cliente."
        )

except KeyboardInterrupt:
    print("\n")
    print(f"[{horario()}] Servidor interrompido pelo usuário.")

except OSError as erro:
    print(f"[{horario()}] Erro no servidor: {erro}")

finally:
    servidor.close()
    print(f"[{horario()}] Servidor encerrado.")
    print("=" * 55)
