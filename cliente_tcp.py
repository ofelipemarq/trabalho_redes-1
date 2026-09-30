import socket
import struct
from datetime import datetime


PORTA = 1220


def horario():
    return datetime.now().strftime("%H:%M:%S")


def receber_exatamente(conexao, quantidade):
    dados = b""

    while len(dados) < quantidade:
        parte = conexao.recv(quantidade - len(dados))

        if not parte:
            return None

        dados += parte

    return dados


def receber_mensagem(conexao):
    cabecalho = receber_exatamente(conexao, 4)

    if cabecalho is None:
        return None

    tamanho = struct.unpack("!I", cabecalho)[0]

    dados = receber_exatamente(conexao, tamanho)

    if dados is None:
        return None

    return dados.decode("utf-8")


def enviar_mensagem(conexao, mensagem):
    dados = mensagem.encode("utf-8")

    cabecalho = struct.pack("!I", len(dados))

    conexao.sendall(cabecalho + dados)


print("=" * 55)
print("CLIENTE TCP")
print("=" * 55)

HOST = input("Digite o IP do servidor: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print(
        f"[{horario()}] "
        f"Conectando a {HOST}:{PORTA}..."
    )

    cliente.connect((HOST, PORTA))

    print(
        f"[{horario()}] "
        "Conexão TCP estabelecida."
    )

    nome = input("Digite seu nome: ")

    enviar_mensagem(
        cliente,
        nome
    )

    print("\n" + "-" * 55)
    print("Chat iniciado.")
    print("Digite 'sair' para encerrar.")
    print("-" * 55)

    while True:
        mensagem = input(f"\n[{horario()}] {nome}: ")

        enviar_mensagem(
            cliente,
            mensagem
        )

        resposta = receber_mensagem(cliente)

        if resposta is None:
            print(
                f"[{horario()}] "
                "Servidor encerrou a conexão."
            )
            break

        print(
            f"[{horario()}] "
            f"Servidor: {resposta}"
        )

        if mensagem.lower() == "sair":
            break

except ConnectionRefusedError:
    print(
        f"[{horario()}] "
        "Conexão recusada. "
        "Verifique se o servidor está em execução."
    )

except OSError as erro:
    print(
        f"[{horario()}] "
        f"Erro na conexão: {erro}"
    )

finally:
    cliente.close()

    print(
        f"\n[{horario()}] "
        "Conexão encerrada."
    )
    print("=" * 55)