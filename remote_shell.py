import socket
from core import Core, Daemon
from _thread import *


host = "0.0.0.0"
port = 9002
core = Core()
version = "v0.1-dev"
help_text = """
Commands:
/help - display this message
/daemonlist - display list of daemons 
/getlog [name] - get log of daemon
/stop [name] - stop daemon by name
/restart [name] - restart daemon by name
/start [name] - start daemon by name
/stopAll - stop all daemons
/startAll - start all daemons
/restartA;; - restart all daemons
/ver or /version - display version
/getservicefile [name] - display service file of daemon
/list-running - display list of running daemons
/list-stopped - display list of stopped daemons
/exit - disconnect\n
"""

#there are you can store permited to login accounts like a tuple (login,pass) in this list
ACCOUNTS = [("Admin",'123456')]

def client_handler(conn):
    conn.send("SystemD Remote Shell - connection established.\nPlease, login (name and key in one line):\n".encode())
    authed = False
    while True:
        data = conn.recv(2048)
        if not data:
            break
        command_got = data.decode().replace("\n", '')
        print(command_got)
        if authed:
            if command_got == "/daemonlist":
                conn.send("List of daemons.\nNAME - CATEGORY - STATUS\n____________________________\n".encode())
                conn.send(core.getDaemonList().encode())
            elif command_got == '/list-running':
                conn.send(core.getRunningDaemons().encode())
            elif command_got == "/list-stopped":
                conn.send(core.getStoppedDaemons().encode())
            elif command_got == "/restartAll":
                conn.send(core.restartAllDaemons().encode())
            elif command_got == "/stopAll":
                conn.send(core.stopAllDaemons().encode())
            elif command_got == "/startAll":
                conn.send(core.startAllDaemons().encode())
            elif command_got.find("/start ") != -1:
                name = command_got.split(' ')[1]
                conn.send(core.startDaemon(name).encode())
            elif command_got.find("/restart ") != -1:
                name = command_got.split(' ')[1]
                conn.send(core.restartDaemon(name).encode())
            elif command_got.find("/stop ") != -1:
                name = command_got.split(' ')[1]
                conn.send(core.stopDaemon(name).encode())
            elif command_got == '/exit':
                break
            elif command_got.find("/getservicefile ")!=-1:
                name = command_got.split(' ')[1]
                conn.send(core.daemons_list[name].getServiceFile().encode())
            elif command_got == '/ver' or command_got=="/version":
                conn.send(f"SystemD Remote Shell\nCore version: {core.version}\nShell version: {version}\nCreated by Ebobalik\n".encode())
            elif command_got.find("/getlog ")!=-1:
                name = command_got.split()[1]
                conn.send(core.daemons_list[name].getLog().encode())

            elif command_got == '/help':

                conn.send(help_text.encode())
            else:
                conn.send("Unknown command. Try to use /help for call list of commands\n".encode())
        else:
            if tuple(command_got.split(' ')) in ACCOUNTS:
                authed = True
                conn.send("You are welcome\n".encode())
            else:
                conn.send("Authentication failed\n".encode())
                break
    conn.close()

def accept_connections(ServerSocket):
    client, addr = ServerSocket.accept()
    print(f'Connected to: {addr[0]}:{addr[1]}')
    start_new_thread(client_handler, (client,))

def start_server(host,port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host,port))
    except socket.error as e:
        print(str(e))
        exit()
    print(f"SystemD Remote Shell started on port {port}")
    ServerSocket.listen()
    while True:
        accept_connections(ServerSocket)

if __name__ == '__main__':
    start_server(host,port)
