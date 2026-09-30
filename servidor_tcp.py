import socket
import struct
from datetime import datetime


HOST = "0.0.0.0"
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
    # Cabeçalho de 4 bytes contendo o tamanho da mensagem
    cabecalho = receber_exatamente(conexao, 4)

    if cabecalho is None:
        return None

    tamanho = struct.unpack("!I", cabecalho)[0]

    # Recebe exatamente a quantidade informada no cabeçalho
    dados = receber_exatamente(conexao, tamanho)

    if dados is None:
        return None

    return dados.decode("utf-8")


def enviar_mensagem(conexao, mensagem):
    dados = mensagem.encode("utf-8")

    # Inteiro de 4 bytes em ordem de rede
    cabecalho = struct.pack("!I", len(dados))

    conexao.sendall(cabecalho + dados)


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reutilizar a porta rapidamente após reiniciar o servidor
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    servidor.bind((HOST, PORTA))
    servidor.listen(1)

    print("=" * 55)
    print("SERVIDOR TCP")
    print("=" * 55)
    print(f"[{horario()}] Servidor iniciado.")
    print(f"[{horario()}] Aguardando conexões na porta {PORTA}...")

    while True:
        conexao, endereco_cliente = servidor.accept()

        ip_cliente = endereco_cliente[0]
        porta_cliente = endereco_cliente[1]

        print("\n" + "-" * 55)
        print(f"[{horario()}] Nova conexão recebida.")
        print(f"IP do cliente: {ip_cliente}")
        print(f"Porta do cliente: {porta_cliente}")

        with conexao:
            nome = receber_mensagem(conexao)

            if nome is None:
                print(
                    f"[{horario()}] Cliente desconectou "
                    "antes de se identificar."
                )
                continue

            print(f"Nome do cliente: {nome}")
            print("-" * 55)

            while True:
                mensagem = receber_mensagem(conexao)

                if mensagem is None:
                    print(
                        f"\n[{horario()}] "
                        f"{nome} encerrou a conexão inesperadamente."
                    )
                    break

                print(
                    f"[{horario()}] "
                    f"{nome}: {mensagem}"
                )

                if mensagem.lower() == "sair":
                    enviar_mensagem(
                        conexao,
                        "Conexão encerrada pelo servidor."
                    )

                    print(
                        f"[{horario()}] "
                        f"{nome} solicitou encerramento."
                    )
                    break

                resposta = (
                    f"Mensagem de {nome} recebida com sucesso!"
                )

                enviar_mensagem(
                    conexao,
                    resposta
                )

        print(
            f"[{horario()}] "
            "Conexão com o cliente encerrada."
        )
        print(
            f"[{horario()}] "
            "Aguardando novo cliente..."
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