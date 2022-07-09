import random
from C_U import *
import os
import sys
import socket
import subprocess
import pickle
import time

n=5
num_res=random.randint(n//2,n)
res=[]
res=random.sample(range(1,n+1),num_res)
pes=[]
for i in range(len(res)):
    # only take in res[i] who is not user_cur
    if res[i]!=int(user_cur[4:]):
        pes.append(res[i])
res=pes
print("I need to send these resources:",res)
for i in range(len(res)):
    res[i]=f"{user_cur[4:]} {res[i]}"


# send to writer.py
ip = subprocess.check_output(["ifconfig", "wlo1"]).decode("utf-8").split("\n")[1].split()[1]

freed=False
def send(message):
    # send the message until the receiver sends an ACK
    while True:
      #  print("Hel")
        # make connection using socket
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.connect((ip, int(3220)))
            # send the message
            sock.send(pickle.dumps(message))
            # receive the ACK
            ack = sock.recv(1024)
            ack=ack.decode("utf-8")
            print(ack)
            flag=1
            if ack=="Yes it is in deadlock":
                # wait for random time to sleep
                time.sleep(random.randint(1,10))
                flag=0
            elif ack=="Done":
                break
            else:
                 # wait for random time to use the resource
                time.sleep(random.randint(1,5))
                flag=0
                
            sock.close()
            # if the ACK is received, break the loop
            if flag:
                break
        except:
            pass


# send res to writer.py
send(res)
