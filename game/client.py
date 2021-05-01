import socket
import threading
import pickle

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.65.183"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def receve_pickle():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length)
        return pickle.loads(msg)

def recive():
    wrapped_msg = receve_pickle()
    if wrapped_msg[0] == DISCONNECT_MESSAGE:
        client.send("Leaving message".encode(FORMAT))
        # przydolby sie usuwac z dicta rozlaczonego gracza
        client.close()
    elif wrapped_msg[0] == "YOUR PLAYER":
        print(wrapped_msg[1])
    elif wrapped_msg[0] == "CHOOSE MOVE":
        print("Co robisz?")
        send(input())
    elif wrapped_msg[0] == "OPPONENT":
        print(wrapped_msg[1])
    elif wrapped_msg[0] == "CARDS":
        print(wrapped_msg[1])
    elif wrapped_msg[0] == "WINNERS":
        print("WINNERS:")
        print(wrapped_msg[1])
    else:
        return wrapped_msg[0]


#def recive():
   # msg_length = client.recv(HEADER).decode(FORMAT)
   # if msg_length:
     #   msg_length = int(msg_length)
       # msg = client.recv(msg_length).decode(FORMAT)
       # if msg == DISCONNECT_MESSAGE:
       #     client.send("Leaving message".encode(FORMAT))
            # przydolby sie usuwac z dicta rozlaczonego gracza
         #   client.close()
      #  elif msg == "YOUR PLAYER":
         #   send("OK waiting for it")
         #   print(recive_pickle())
       # elif msg == "CHOOSE MOVE":
        #    print("Co robisz?")
        #    send(input())
       # elif msg == "OPPONENT":
        #    send("OK gimme his info")
        #    print(recive_pickle())
      #  elif msg == "CARDS":
        #    send("OK gimmie info about cards")
         #   print(recive_pickle())
      #  elif msg == "WINNERS":
        #    send("OK gimmie info who won")
        #    print(recive_pickle())
       # else:
      #      return msg



def listening():
    while connected:
        recive()



connected = True
thread = threading.Thread(target=listening, args=())
thread.start()
nick = str(input("Podaj nick: "))
send(nick)

