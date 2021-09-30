import socket
import threading

host = '0.0.0.0'
port = 10004

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive():
    print("[rThread - receive] start")
    while True:
        try:
            message = (client.recv(1024)).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("Error occurred!")
            client.close()
            break
    print("[rThread - receive] end")


def write():
    print("[wThread - write] start")
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


if __name__ == '__main__':
    nickname = input("choose a nickname: ")

    print("rThread")
    rThread = threading.Thread(target=receive)
    rThread.start()

    print("wThread")
    wThread = threading.Thread(target=write)
    wThread.start()
