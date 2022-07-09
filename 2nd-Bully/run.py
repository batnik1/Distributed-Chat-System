users=5
messages=50

# make 10 new folders
import os
import random
try:
    for i in range(1,users+1):
        os.mkdir(f"user{i}")
except:
    pass
# find public ip address from ifconfig
import subprocess
ip = subprocess.check_output(["ifconfig", "wlo1"]).decode("utf-8").split("\n")[1].split()[1]
# print(ip)

initial_port=2880
# create a text file named text.txt deleting any previously existing file in each folder
with open(f"text.txt", "w") as f:
    f.write("Users\n")
    for i in range(1,users+1):
        cur_port=initial_port+i
        # write "IP" in second line with port number, with user name 
        f.write(f"{ip},{cur_port},user{i}\n")
    f.write("Message")
    for i in range(1,messages+1):
        # choose a random sender and receiver and they must be different
        sender,receiver=random.sample(range(1,users+1),2)
        message="Hi from" + f" user{sender} to user{receiver} with message number {i}"
        f.write(f"\nuser{sender},user{receiver},{message}")

# copy this file to each folder
import shutil
for i in range(1,users+1):
    shutil.copy("L_e_r_1.py", f"user{i}")
    # change first line of C_U.py to user_cur="user{i}"
    with open(f"C_U.py", "r") as f:
        lines = f.readlines()
        lines[0] = f"user_cur=\"user{i}\"\n"
        lines[1]=f"total_members={users}\n" 
    with open(f"C_U.py", "w") as f:
        f.writelines(lines)
    shutil.copy("C_U.py", f"user{i}")

# now run sender_receiver.py in each folder
for i in range(1,users+1):
    # start a terminal in each folder and run sender_receiver.py from there
    os.chdir(f"user{i}")
    # start a terminal in each folder and run sender_receiver.py from there
    os.system(f"gnome-terminal -e 'bash -c \"python3 L_e_r_1.py; exec bash\"'")
    os.chdir("..")

    # # # run sender_receiver.py
    # # os.system("python3 sender_receiver.py")
    # os.chdir("..")





input()



# delete those folders with subfiles and subfolders
for i in range(1,users+1):
    os.system(f"rm -rf user{i}")

os.system("kill -9 $(pgrep bash)")
os.system("kill -9 $(pgrep bash)")
os.system("kill -9 $(pgrep bash)")
os.system("kill -9 $(pgrep bash)")
