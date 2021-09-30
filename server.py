import socket
import threading

host = '0.0.0.0'  # localhost
port = 10004

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message.encode('ascii'))


def handle(client):
    while True:
        try:
            message = (client.recv(1024)).decode('ascii')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"[HANDLE] {nickname} has left the chat.")
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"[SERVER] {address} connected to the server")

        client.send('NICK'.encode('ascii'))
        nickname = (client.recv(1024)).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"[SERVER] {address} has set their nickname to {nickname}")
        broadcast(f"{nickname} joined the server!")
        client.send("You have successfully connected to the server.".encode('ascii'))

        cThread = threading.Thread(target=handle, args=(client,))
        cThread.start()


if __name__ == '__main__':
    print("Listening to connections...")
    receive()
