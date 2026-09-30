import socket
from datetime import datetime


PORTA = 1220
BUFFER = 1024
TIMEOUT = 5


def horario():
    return datetime.now().strftime("%H:%M:%S")


print("=" * 55)
print("CLIENTE UDP")
print("=" * 55)

HOST = input("Digite o IP do servidor: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Evita que o cliente fique esperando para sempre
# caso a resposta UDP não chegue.
cliente.settimeout(TIMEOUT)

servidor = (HOST, PORTA)

try:
    print(
        f"[{horario()}] "
        f"Servidor definido como {HOST}:{PORTA}"
    )

    print("\n" + "-" * 55)
    print("Digite mensagens para enviar.")
    print("Digite 'sair' para encerrar.")
    print("-" * 55)

    while True:
        mensagem = input(f"\n[{horario()}] Você: ")

        cliente.sendto(
            mensagem.encode("utf-8"),
            servidor
        )

        print(
            f"[{horario()}] "
            "Datagrama enviado."
        )

        try:
            dados, endereco = cliente.recvfrom(BUFFER)

            resposta = dados.decode("utf-8")

            print(
                f"[{horario()}] "
                f"Servidor: {resposta}"
            )

        except socket.timeout:
            print(
                f"[{horario()}] "
                "Tempo limite atingido: nenhuma resposta recebida."
            )

        if mensagem.lower() == "sair":
            break

except OSError as erro:
    print(
        f"[{horario()}] "
        f"Erro no cliente: {erro}"
    )

finally:
    cliente.close()

    print(
        f"\n[{horario()}] "
        "Cliente UDP encerrado."
    )
    print("=" * 55)
