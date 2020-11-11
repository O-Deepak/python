
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 5000
bufferSize = 1024
address = (HOST, PORT)
socket = socket(AF_INET, SOCK_STREAM)
socket.bind(address)


def acceptConnection():

    while True:
        client, clientAddress = socket.accept()
        print("%s:%s has connected." % clientAddress)
        client.send("Create your own server and begin texting! ".encode("utf8"))
        client.send("Type your name and press enter!".encode("utf8"))
        addresses[client] = clientAddress
        Thread(target=handleClient, args=(client, clientAddress)).start()

def broadcastMsgs(msg, prefix=""):  

    for socket in clients:
        socket.send(bytes(prefix, "utf8") + msg)

def handleClient(conn, address): 
    name = conn.recv(bufferSize).decode("utf8")
    welcome = 'Welcome %s!!!' % name
    conn.send(bytes(welcome, "utf8"))
    msg = "%s from [%s] has joined the chatroom!" % (name, "{}:{}".format(address[0], address[1]))
    broadcastMsgs(bytes(msg, "utf8"))
    clients[conn] = name
    while True:
        msg = conn.recv(bufferSize)
        if msg != bytes("#quit", "utf8"):
            broadcastMsgs(msg, name + ": ")
        else: 
            qu= '%s has left the chatroom.' % name
            broadcastMsgs(bytes(qu,"utf8"))
            del clients[conn]
            conn.send(bytes("#quit", "utf8"))
            break


if __name__ == "__main__":
    socket.listen(5)  
    print("Chat Server has Started !!")
    print("Waiting for your friends to join...")
    threadAccept = Thread(target=acceptConnection)
    threadAccept.start()  
    threadAccept.join()
    socket.close()
