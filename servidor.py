from socket import *
import json
import _thread

serverPort = 3001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(True)

comandos = ["somar", "subtrair", "multiplicar", "dividir", "modulo"]

def execucao(connection, client):
    print(connection)
    print(client)

    while True:
        received = connection.recv(1024)
        print("Dados recebidos em requisição: {}".format(received))

        receivedsData = json.loads(received)

        print("Os parametros recebidos para a operação foram: {} e {}".format(receivedsData["value_A"],receivedsData["value_B"]))
        print("A chave de operação é {}".format(receivedsData["key"]))


        print(received)

        if (receivedsData["operation"] in comandos):
            aux1,aux2 = receivedsData["value_A"],receivedsData["value_B"]
            if receivedsData["operation"] == "soma":
                result = int(aux1) + int(aux2)
            elif receivedsData["operation"] == "subtrair":
                result = int(aux1) - int(aux2)
            elif receivedsData["operation"] == "multiplicar":
                result = int(aux1)*int(aux2)
            elif receivedsData["operation"] == "modulo":
                result = int(aux1)%int(aux2)
            else:
                result = int(aux1)/int(aux2)
            response = {"requestId": receivedsData["requestId"], "response_op": result, "statusCode": "200", "message": "OK"}
            connection.send(json.dumps(response).encode(encoding='utf-8'))

        if (receivedsData["operation"] == "sair"):
            response = {"requestId": receivedsData["requestId"], "message": "operation terminated by the client"}
            connection.send(json.dumps(response).encode(encoding='utf-8'))
            print("Finish Comunication")
            break
        
        if (receivedsData["operation"] not in comandos):
            response = {"requestId": receivedsData["requestId"], "errorCode": "402", "message": "Operation unavailable"}
            connection.send(json.dumps(response).encode(encoding='utf-8'))


    connection.close()
            

print("The server is ready to receive")
while True:
    print("Waiting from Client")
    connection, addr = serverSocket.accept()
    _thread.start_new_thread(execucao, (connection, addr))