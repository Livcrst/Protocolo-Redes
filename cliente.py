from socket import *
import json
import random

serverName = "localhost"
serverPort = 3001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


def operacao():
    requestId = random.randint(1, 10000)
    operation = input("Digite a operação desejada (toda minúscula): ")
    a = input("Digite o primeiro numero: ")
    b = input("Digite o segundo numero: ")
    key = "RC"

    data = {"requestId": requestId, "operation": operation, "value_A": a, "value_B": b,
            "key": key}

    return json.dumps(data)


while True:
    comando = operacao()
    clientSocket.send(comando.encode(encoding='utf-8'))
    print("waiting to be sent")
    novocomando = clientSocket.recv(1024)
    print("operation sent")
    print("From server: ", novocomando)

    objet = json.loads(comando)
    if (objet["operation"] == "sair"):
        break

clientSocket.close()