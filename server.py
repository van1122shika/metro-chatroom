import socket 
import threading 
host = '10.12.27.115'
port = 9090
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
nicknames = []
#broadcast
def broadcast(message):
    for client in clients:
        client.send(message)

#handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} : {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!\n".encode('utf-8'))
            nicknames.remove(nickname)
            break
#recieve 
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!\n")
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}\n")
        broadcast(f"{nickname} joined the chat!\n".encode('utf-8'))
        client.send('Connected to the server!\n'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
    
print("Server running...")
recieve()