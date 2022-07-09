import random

from pygame import init
from C_U import *
import os
import sys
import socket
import subprocess
import pickle
import time

leader=total_members
ip = subprocess.check_output(["ifconfig", "wlo1"]).decode("utf-8").split("\n")[1].split()[1]
# port from C_U.py
port=int(user_cur[4:])+4500
def receive():
    # make connection using socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # do this
        sock.bind((ip, port))
        # listen only for random sec 
        sock.settimeout(random.randint(2,4))
        sock.listen(1)
        # accept the connection
        conn, addr = sock.accept()
        # receive the message
        message = conn.recv(1024)
        message = pickle.loads(message)
        if message=="Alive?":
            # send him an ACK
            print("ALive message")
            conn.send(pickle.dumps("ACK"))
            return 1
        elif message[0]=="New_Leader":
            leader=int(message[1])
            conn.send(pickle.dumps("ACK"))
            return -1,leader
        else:
            pass
        #    print("Message Received")
        conn.close()
    except:
        #print("Passed")
        pass
    return 0

def send(user):
    # send the message with a "HI" to any random user in the system
    port_to_send=4500+user
    # make connection using socket
    try:
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((ip, port_to_send))
        # send the message
        sock.send(pickle.dumps("HI"))
        # receive the ACK
      #  ack = sock.recv(1024)
        sock.close()
        # if the ACK is received, break the loop
        #print("Passed sending a message to user"+str(user))
        return 1
    except:
     #   print("Failed")
        return 0

def sends(user,flag=False):
    # send the message with a "HI" to any random user in the system
    port_to_send=4500+user
    # make connection using socket
    try:
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((ip, port_to_send))
        # send the message
        if flag==False:
            sock.send(pickle.dumps("Alive?"))
        else:
            # send list flagk
            flagk=["New_Leader",flag]
            sock.send(pickle.dumps(flagk))
        ack=sock.recv(1024)
        sock.close()
        ack=pickle.loads(ack)
        if ack=="ACK":
            return "OK"
        # receive the ACK
      #  ack = sock.recv(1024)
        
        # if the ACK is received, break the loop
      #  print("Passed sending a message to user"+str(user))
    except:
        pass
    return "NOT OK"

print(ip,port,user_cur)
flag=0
count=0
initiator=False
inititator_list=[]
responses=0
county=0
candidate=False
cur_response=0
termination=False
termination_list=[]
termination_county=0
latest_time=time.time()

while 1:
    check=receive()
    if check==1:
        if time.time()-latest_time>15:
            initiator=True
    elif check!=0:
        leader=check[1]
        initiator=False
        inititator_list=[]
        responses=0
        flag=0
        county=0
        termination=False
        print("Got a new_leader, new leader is:",leader)
        latest_time=time.time()


    # random number out of 1 to 10
    if initiator==False and termination==False:
        if flag==0:
            num=random.randint(1,10)
            flag=1
            user=int(user_cur[4:])
            while user==int(user_cur[4:]):
            # print(user,user_cur,"ldu")
                user=random.randint(1,leader)
        if num>-3: # testing condition no use
            if send(user):
                flag=0
                count=0
            else:
                count+=1
                if count>5:
                    if user==leader:
                        print(f"Leader - {leader} is not online, call an election guys")
                        initiator=True
                        # initiator_list=> all users bigger than cur_user
                        for i in range(1,leader+1):
                            if i>int(user_cur[4:]):
                                inititator_list.append(i)
                        print(inititator_list,"INITITATOR LIST")
                        if len(inititator_list)==0:
                            print("No one is online, I am the leader")
                            leader=int(user_cur[4:])
                            initiator=False
                            inititator_list=[]
                            responses=0
                            flag=0
                            continue

                        responses=len(inititator_list)
                        cur_response=0
                        county=0
                        candidate=True
                       # print(user_cur,inititator_list)
                    flag=0
                    count=0
    elif termination==False and initiator==True:
        # start sending messages to everyone in the initiator_list
        if len(inititator_list)==0:
            # print("Original leader was",leader," I am becoming new leader since the no one above me is responding   ")
            # print("Election over, I am the leader",user_cur)
            initiator=False
            inititator_list=[]
         #   leader=int(user_cur[4:])
            termination=True
            # send everyone a message saying that I am the leader
            for i in range(1,total_members+1):
                if i!=int(user_cur[4:]):
                    termination_list.append(i)
            print("Termination list",termination_list)
            continue
        x=sends(inititator_list[-1])
        if x=="OK":
            initiator=False
            inititator_list=[]
            print("OK")
            continue
        else:
            county+=1
        
        if county==5:
            inititator_list.pop()
            county=0
        if len(inititator_list)==0:
            # print("Original leader was",leader," I am becoming new leader since the no one above me is responding   ")
            # print("Election over, I am the leader",user_cur)
            initiator=False
            inititator_list=[]
           # leader=int(user_cur[4:])
            termination=True
            # send everyone a message saying that I am the leader
            for i in range(1,leader+1):
                if i!=int(user_cur[4:]):
                    termination_list.append(i)
            print("Termination list",termination_list)
    elif termination==True:
        if len(termination_list)==0:
            print(termination,initiator,leader)
            print("Everyone_knows_I_am_the_leader",user_cur)
            termination=False
            leader=int(user_cur[4:])
            initiator=False
            inititator_list=[]
            termination_list=[]
            continue
        x=sends(termination_list[-1],flag=int(user_cur[4:]))
        if x=="OK":
            termination_list.pop()
            termination_county=0
        else:
            termination_county+=1
        
        if termination_county==5:
            termination_list.pop()
            termination_county=0
        if len(termination_list)==0:
            print(termination,initiator,leader)
            print("Everyone_knows_I_am_the_leader",user_cur)
            termination=False
            leader=int(user_cur[4:])
            initiator=False
            inititator_list=[]
            termination_list=[]





