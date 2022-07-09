from C_U import *
class User:
    def __init__(self,ip,port,username):
        self.ip=ip
        self.port=port
        self.username=username

class Message:
    def __init__(self,sender,receiver,message):
        self.sender=sender
        self.receiver=receiver
        self.message=message

class Identity:
    def __init__(self,username):
        self.username=username

ID=Identity(user_cur)
print(user_cur+" is running")
# read text.txt file
messages=[] 
user_info=[]
user_map={}
stripper=0
def read_file():
    with open("text.txt","r") as f:
        stripper=0
        for line in f:
            if line[:5]=="Users":
                stripper=0
                continue
            elif line[:4]=="Mess":
                stripper=1
                continue
            elif stripper==0:
                ip,port,username=line.split(",")
                username=username.strip()
                user_info.append(User(ip,port,username))
                user_map[username]=user_info[-1]
            elif stripper==1:
                #print(user_map)
                sender,receiver,message=line.split(",")
                messages.append(Message(user_map[sender],user_map[receiver],message))




read_file()

