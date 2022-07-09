# send and receive messages through terminal netcat
import os
import sys
from user import *
import socket

def send(sender,receiver,message):
    # send the message until the receiver sends an ACK
    while True:
      #  print("Hel")
        # make connection using socket
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.connect((receiver.ip, int(receiver.port)))
            # send the message
            sock.send(message.encode())
            # receive the ACK
            por_re=sock.recv(1024)
            if por_re.decode()=="port":
                # send senders port
                sock.send(sender.port.encode())
            ack = sock.recv(1024)
            # close the socket
            sock.close()
            # if the ACK is received, break the loop
            if ack.decode() == "ACK":
                   # print("Ack received")
                    break
        except:
            pass
     #   break

def receive(receiver,sender):
    # make connection using socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # do this
    sock.bind((receiver.ip, int(receiver.port)))
    while True:
        sock.listen(1)
        # accept the connection
        conn, addr = sock.accept()
        # receive the message
        message = conn.recv(1024)
        conn.send("port".encode())
        # send an acknowledgement
        port=conn.recv(1024)
        if int(port.decode())==int(sender.port):
            conn.send("ACK".encode())
            print(message.decode())
            break
        else:
            conn.send("NON-ACK".encode())
    # close the socket
    conn.close()
    
    





for mess in messages:
    # check the name of the sender and receiver
    if ID.username == mess.sender.username:
        send(mess.sender,mess.receiver,mess.message)
    elif ID.username == mess.receiver.username:
        receive(mess.receiver,mess.sender)

