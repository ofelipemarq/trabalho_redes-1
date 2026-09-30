# Comunicação Cliente-Servidor com TCP e UDP

Projeto desenvolvido para estudo prático da **camada de transporte**, com implementação de aplicações cliente-servidor utilizando os protocolos **TCP** e **UDP** em Python.

O objetivo é demonstrar, na prática, diferenças importantes entre os dois protocolos, como estabelecimento de conexão, fluxo de bytes, datagramas, confiabilidade, identificação do remetente e tratamento de falhas.

---

## Funcionalidades

### TCP

- Conexão cliente-servidor com `SOCK_STREAM`
- Cliente informa dinamicamente o IP do servidor
- Identificação do cliente por nome
- Troca de várias mensagens na mesma conexão
- Servidor atende múltiplos clientes de forma sequencial
- Encerramento controlado com o comando `sair`
- Tratamento de desconexões e erros
- Reutilização da porta com `SO_REUSEADDR`
- Delimitação das mensagens com cabeçalho de 4 bytes
- Leitura completa da mensagem mesmo quando os dados chegam em partes
- Logs com horário, IP e porta do cliente

### UDP

- Comunicação cliente-servidor com `SOCK_DGRAM`
- Envio e recebimento com `sendto()` e `recvfrom()`
- Troca de várias mensagens
- Identificação do IP e da porta de origem de cada datagrama
- Timeout no cliente para evitar espera indefinida
- Encerramento do cliente com o comando `sair`
- Servidor permanece disponível após o encerramento de um cliente
- Tratamento de erros
- Logs com horário

---

## Tecnologias utilizadas

- **Python 3**
- Biblioteca padrão `socket`
- Biblioteca padrão `struct`
- Biblioteca padrão `datetime`
- **Linux**
- Terminal
- SSH e SCP para testes em máquina remota

Não são necessárias bibliotecas externas.

---

## Ambientes utilizados

O projeto foi desenvolvido e testado em:

- computador cliente com **Fedora Linux**
- servidor Linux remoto da universidade
- comunicação local utilizando `127.0.0.1`
- comunicação entre máquinas pela rede da universidade

> O endereço IP do servidor remoto não é fixado no código do cliente. Ele é informado no momento da execução.

---

## Estrutura do repositório

```text
.
├── cliente_tcp.py
├── servidor_tcp.py
├── cliente_udp.py
├── servidor_udp.py
└── README.md
```

---

## Porta utilizada

Os programas utilizam uma porta definida no código:

```python
PORTA = 1220
```

Em ambiente acadêmico, a porta pode ser definida de acordo com a regra determinada para a atividade.

Caso seja necessário utilizar outra porta, altere o mesmo valor no cliente e no servidor correspondentes.

---

# Execução

## 1. Teste local

Para testar na mesma máquina, abra dois terminais.

### TCP

No primeiro terminal:

```bash
python3 servidor_tcp.py
```

No segundo:

```bash
python3 cliente_tcp.py
```

Quando o cliente solicitar o IP do servidor, informe:

```text
127.0.0.1
```

O cliente solicitará um nome e, em seguida, permitirá o envio de mensagens.

Para encerrar:

```text
sair
```

O servidor continuará em execução e poderá aceitar um novo cliente.

---

### UDP

No primeiro terminal:

```bash
python3 servidor_udp.py
```

No segundo:

```bash
python3 cliente_udp.py
```

Quando solicitado, informe:

```text
127.0.0.1
```

Digite as mensagens normalmente.

Para encerrar o cliente:

```text
sair
```

O servidor UDP continuará aguardando novos datagramas.

---

## 2. Teste entre duas máquinas

No servidor remoto, execute:

```bash
python3 servidor_tcp.py
```

ou:

```bash
python3 servidor_udp.py
```

No computador cliente, execute o programa correspondente:

```bash
python3 cliente_tcp.py
```

ou:

```bash
python3 cliente_udp.py
```

Quando solicitado, informe o endereço IP da máquina em que o servidor está sendo executado.

> As duas máquinas precisam conseguir se comunicar pela rede e a porta utilizada deve estar acessível.

---

## Enviando os arquivos para um servidor remoto

Os arquivos podem ser enviados utilizando `scp`.

Exemplo:

```bash
scp cliente_tcp.py servidor_tcp.py cliente_udp.py servidor_udp.py usuario@IP_DO_SERVIDOR:~/sprint-redes/transporte/
```

Para acessar o servidor:

```bash
ssh usuario@IP_DO_SERVIDOR
```

Depois:

```bash
cd ~/sprint-redes/transporte
ls
```

---

# Como a aplicação TCP funciona

O TCP é um protocolo orientado a conexão.

O servidor:

1. cria um socket TCP;
2. associa o socket a uma porta com `bind()`;
3. entra em modo de escuta com `listen()`;
4. aguarda um cliente com `accept()`;
5. troca mensagens com o cliente;
6. encerra apenas aquela conexão;
7. volta a aguardar outro cliente.

O cliente estabelece a conexão utilizando:

```python
connect()
```

Depois disso, cliente e servidor podem trocar vários dados utilizando a mesma conexão.

---

## Delimitação das mensagens TCP

TCP fornece um **fluxo de bytes**. Por isso, uma chamada a `sendall()` não corresponde necessariamente a uma única chamada a `recv()`.

Uma mensagem pode chegar dividida em várias partes ou ser agrupada com outros dados.

Para evitar esse problema, a aplicação utiliza um pequeno protocolo próprio.

Cada mensagem possui:

```text
┌────────────────────┬──────────────────────┐
│ Cabeçalho: 4 bytes │ Conteúdo da mensagem │
└────────────────────┴──────────────────────┘
```

O cabeçalho informa o tamanho da mensagem.

Exemplo conceitual:

```text
[ tamanho = 10 ][ mensagem ]
```

O tamanho é convertido para 4 bytes utilizando:

```python
struct.pack("!I", tamanho)
```

O receptor primeiro lê o cabeçalho e depois continua chamando `recv()` até receber exatamente a quantidade de bytes esperada.

Isso evita depender da forma como o TCP divide os dados durante o transporte.

---

# Como a aplicação UDP funciona

UDP é orientado a **datagramas** e não exige o estabelecimento de uma conexão antes da troca de dados.

O cliente envia diretamente utilizando:

```python
sendto()
```

O servidor recebe utilizando:

```python
recvfrom()
```

O `recvfrom()` retorna:

```text
dados + endereço do remetente
```

Dessa forma, o servidor consegue identificar o IP e a porta de origem de cada datagrama.

Diferentemente do TCP, o UDP não garante:

- entrega;
- retransmissão;
- ordenação;
- controle de conexão.

Por esse motivo, o cliente utiliza um **timeout**. Caso nenhuma resposta seja recebida dentro do período definido, o programa informa que o tempo limite foi atingido em vez de permanecer bloqueado indefinidamente.

---

# TCP x UDP neste projeto

| Característica | TCP | UDP |
|---|---|---|
| Tipo | Fluxo de bytes | Datagramas |
| Orientado a conexão | Sim | Não |
| Estabelecimento de conexão | `connect()` / `accept()` | Não existe |
| Envio | `sendall()` | `sendto()` |
| Recebimento | `recv()` | `recvfrom()` |
| Garantia de entrega | Sim | Não |
| Ordem dos dados | Preservada pelo protocolo | Não garantida |
| Delimitação de mensagens | Implementada pela aplicação | Preservada por datagrama |
| Timeout da aplicação | Não utilizado no fluxo principal | Utilizado no cliente |

---

# Encerramento

Nos dois clientes, o comando:

```text
sair
```

encerra a execução do cliente.

No TCP, o servidor fecha a conexão daquele cliente e volta para `accept()`, ficando disponível para outra conexão.

No UDP, não existe uma conexão para ser encerrada. O cliente simplesmente termina sua execução e o servidor continua aguardando outros datagramas.

Para encerrar manualmente o servidor:

```text
Ctrl + C
```

---

# Possíveis erros

## `Connection refused`

Normalmente indica que:

- o servidor TCP não está em execução;
- o IP informado está incorreto;
- a porta utilizada no cliente é diferente da porta do servidor;
- a rede ou firewall está bloqueando a conexão.

## Timeout no UDP

A mensagem de timeout significa que o cliente enviou o datagrama, mas não recebeu uma resposta dentro do tempo configurado.

Isso pode acontecer, por exemplo, se:

- o servidor UDP não estiver em execução;
- o IP ou a porta estiverem incorretos;
- o datagrama ou a resposta não chegarem ao destino.

## Porta já está em uso

Verifique se já existe outra instância do programa utilizando a mesma porta.

No Linux, uma forma de consultar é:

```bash
ss -ltnup
```

---

# Conceitos demonstrados

O projeto permite observar na prática conceitos como:

- sockets;
- arquitetura cliente-servidor;
- endereços IP;
- portas;
- portas efêmeras;
- camada de transporte;
- TCP;
- UDP;
- estabelecimento e encerramento de conexão;
- fluxo de bytes;
- datagramas;
- multiplexação e demultiplexação;
- framing na camada de aplicação;
- timeout;
- tratamento de erros.

---

## Autor

**Felipe Marques**

Projeto acadêmico desenvolvido para estudo de Redes de Computadores e da camada de transporte.
