import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def file_write(msg):
    try:
        with open("data.txt", "a+") as fw:
            fw.write(msg)
    except:
        print("Error occured while handeling the file.")

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            abb = f"{nicknames[clients.index(client)].decode()} says {message.decode()}"
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
            writer = threading.Thread(target=file_write, args=(abb,))
            writer.start()
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
 
def receive():
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}!")
        
            client.send("NICK".encode('utf-8'))
            nickname = client.recv(1024)
        
            nicknames.append(nickname)
            clients.append(client)
        
            print(f"Nickname of the client is {nickname}")
            broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
            client.send("Connected to the server".encode('utf-8'))
        
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            print("Error had occured!")
            break

with open("info.txt", "r") as f:
    about = f.readlines()
    for detail in about:
        print(detail, end="")
print("\n\nServer running...")
receive()

