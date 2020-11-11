

import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def receive():
    
    while True:
        try:
            msg = sock.recv(bufferSize).decode("utf8")
            messageList.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):

    msg = sendMsg.get()
    sendMsg.set("")  # Clears input field.
    sock.send(bytes(msg, "utf8"))
    if msg == "#quit":
        sock.close()
        top.quit()

def onClosing(event=None):
    sendMsg.set("#quit")
    send()

def smileyHappy(event=None):
    sendMsg.set(":)")    # A common smiley character
    send()

def smileySad(event=None):
    sendMsg.set(":(")    # A common smiley character
    send()
def goodmorning(event=None):
    sendMsg.set("Goodmorning")
    send()   
def goodnight(event=None):
    sendMsg.set("Goodnight")
    send()

top = tkinter.Tk()
top.title("Simple Chat Client v1.0")
messageFrame = tkinter.Frame(top)

sendMsg = tkinter.StringVar()  # For the messages to be sent.
sendMsg.set("")
scrollbar = tkinter.Scrollbar(messageFrame)  # To navigate through past messages.
messageList = tkinter.Listbox(messageFrame, height=15, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messageList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messageList.pack()

messageFrame.pack()

button_label = tkinter.Label(top, text="Enter Message:")
button_label.pack()
entry_field = tkinter.Entry(top, textvariable=sendMsg, foreground="Red")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
smiley_button = tkinter.Button(top, text=":)", command=smileyHappy)
smiley_button.pack()
sad_button = tkinter.Button(top, text=":(", command=smileySad)
sad_button.pack()
goodmorning_button = tkinter.Button(top, text="Goodmorning", command=goodmorning)
goodmorning_button.pack()
goodnight_button = tkinter.Button(top, text="Goodnight", command = goodnight)
goodnight_button.pack()


quit_button = tkinter.Button(top, text="Quit", command=onClosing)
quit_button.pack()
  
top.protocol("WM_DELETE_WINDOW", onClosing)



HOST = "127.0.0.1"
PORT = 5000
bufferSize = 1024
address = (HOST, PORT)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(address)

threadReceive = Thread(target=receive)
threadReceive.start()
tkinter.mainloop()  