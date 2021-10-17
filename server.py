import socket
import threading


def broadcast(message):
    for address in clients:
        try:
            clients[address]['client'].send(message.encode('ascii'))
        except BrokenPipeError:
            clients[address]['client'].close()
            clients.pop(address, None)


def handle(client: socket.socket):
    while True:
        try:
            message = (client.recv(1024)).decode('ascii')
            broadcast(message)
        except BrokenPipeError:
            clients.pop(address, None)
            break


def receive(client: socket.socket, address: (str, int)):
    print(f"[SERVER] {address} connected to the server")

    # tmp
    print(f"[SERVER] client: {client}")

    clients[address] = {
        'nickname': None,
        'address': address,
        'client': client
    }

    try:
        clients[address]['client'].send('NICK'.encode('ascii'))
        nickname = (clients[address]['client'].recv(1024)).decode('ascii')
        clients[address]['nickname'] = nickname
    except BrokenPipeError:
        clients[address]['client'].send(f'An error has occurred!'.encode('ascii'))
        clients[address]['client'].close()
        clients.pop(address, None)

    # tmp
    for cl in clients:
        print(f"[SERVER] {cl}: {clients[cl]}")

    print(f"[SERVER] {address} has set their nickname to {clients[address]['nickname']}")
    clients[address]['client'].send("You have successfully connected to the server.".encode('ascii'))
    broadcast(f"{clients[address]['nickname']} joined the server!")

    handle(client)


def execute_commands():
    def get_help():
        help_instructions = \
            "help      : get list of possible commands\n" \
            "online    : see who is online\n" \
            "nicknames : get client's address and their corresponding nickname"
        return help_instructions

    def get_online():
        return clients

    def get_nicknames():
        nicknames = []
        for address in clients:
            nicknames.append((address, clients[address]['nickname']))
        return nicknames

    def default():
        return f"command not found: {command}"

    while True:
        command_raw = str(input())
        if not command_raw:
            command = ''
        else:
            command = command_raw.split()[0]

        commands = {
            'help': get_help,
            'online': get_online,
            'nicknames': get_nicknames
        }

        print(commands.get(command, default)())


if __name__ == '__main__':
    host = '0.0.0.0' # localhost
    port = 10004

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = {}

    execThread = threading.Thread(target=execute_commands)
    execThread.start()

    print("Listening to connections...")

    while True:
        client, address = server.accept()

        recThread = threading.Thread(target=receive, args=(client, address))
        recThread.start()
