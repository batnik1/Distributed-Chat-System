from email.policy import default
import os
import sys
from user import *
import socket
import subprocess
import pickle
import time
from collections import defaultdict


with open("tpoint.txt", "w") as f:
        pass
ip = subprocess.check_output(["ifconfig", "wlo1"]).decode("utf-8").split("\n")[1].split()[1]

occupied_list=defaultdict(list)
Tot=[]
Temp=[]

def receive():
    global Tot,Temp
    print(Tot) # all resources currently occupied
    # make connection using socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # do this
    sock.bind((ip, int(3220)))
    sock.listen(1)
    # accept the connection
    conn, addr = sock.accept()
    # receive the message
    message = conn.recv(1024)
    message = pickle.loads(message)
    # read first line of the message
    lin=""
    for mess in message:
        lin=mess.split()[0]
        break
    if lin in occupied_list:
        print(lin,"has freed its resources")
        # delete the entry
        Sot=[]
        for sec in occupied_list[lin]:
            mess=f"{lin} {sec}"
            Sot.append(mess)
        temps=[]
        for mess in Tot:
            if mess not in Sot:
                temps.append(mess)
        Tot=temps[:]
        del occupied_list[lin]
        conn.send(b"Done")
        return
    # write this message in tpoint.txt
    for mess in message:
        Temp.append(mess)
        fir,sec=mess.split()
        occupied_list[fir].append(sec)
    new=Tot+Temp
    with open("tpoint.txt", "w") as f:
        for mess in new:
            f.write(f"{mess}\n")
    
    # run deadlock.cpp and get the outpput in output variable
    os.system("g++ deadlock.cpp -o deadlock")
    os.system("./deadlock")
    # wait for 2 sec
  #  time.sleep(2)
    # read first line of tpoint.txt
    with open("deads.txt", "r") as f:
        line = f.readline()
        # if line is "Yes it is in deadlock"
        if line == "Yes it is in deadlock\n":
            print("Yes it is in deadlock",lin,"Please wait for some time!!")
            del occupied_list[lin]
            Temp=[]
            # send "Yes it is in deadlock" to writer.py
            conn.send(b"Yes it is in deadlock")
        else:
            print("No it is not in deadlock,",lin,"can use its resources")
            Tot+=Temp
            Temp=[]
            # send "No it is not in deadlock" to writer.py
            conn.send(b"No it is not in deadlock")


    conn.close()

while True:
    receive()
