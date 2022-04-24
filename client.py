import socket
import threading


def receive():
    while True:
        try:
            message = (client.recv(1024)).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        # If something weird gets sent the client.recv method
        except BrokenPipeError:
            print("Error occurred!")
            client.close()
            break
        # If we stop the server while client is running
        except ConnectionResetError:
            print("Server has closed.")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


if __name__ == '__main__':
    host = "141.0.155.230"
    port = 10004
    server = (host, port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to: {host}:{port}")
    client.connect(server)

    nickname = input("choose a nickname: ")

    rThread = threading.Thread(target=receive)
    rThread.start()

    wThread = threading.Thread(target=write)
    wThread.start()
