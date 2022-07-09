with open(f"text.txt", "w") as f:
#     f.write("Users\n")
#     for i in range(1,users+1):
#         cur_port=initial_port+i
#         # write "IP" in second line with port number, with user name 
#         f.write(f"{ip},{cur_port},user{i}\n")
#     f.write("Message")
#     for i in range(1,messages+1):
#         # choose a random sender and receiver and they must be different
#         sender,receiver=random.sample(range(1,users+1),2)
#         message="Hi from" + f" user{sender} to user{receiver} with message number {i}"
#         f.write(f"\nuser{sender},user{receiver},{message}")
