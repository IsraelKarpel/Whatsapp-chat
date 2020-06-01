import sys
from socket import socket, AF_INET, SOCK_DGRAM


def contain(sender, clients_info_loop):
    for x in range(len(clients_info_loop)):
        if cmp(sender, clients_info_loop[x]) == 0:
            return x
    return -1


# list of list: each client has index which contain his msgs
clients_msg = []
# list of tuples
clients_info = []
# list of client names
clients_name = []

string = ""
s = socket(AF_INET, SOCK_DGRAM)
source_ip = '0.0.0.0'
source_port = int(sys.argv[1])
s.bind((source_ip, source_port))

while True:
    string = ""
    data, sender_info = s.recvfrom(2048)
    data2 = data.split(" ", 1)
    client = contain(sender_info, clients_info)

    if client == -1:
        if data2[0] == "1" and len(data2) > 1:
            # send everyone message
            for i in range(len(clients_info)):
                clients_msg[i].append(data2[1] + " " + "has joined")
                if i != len(clients_info) - 1 and len(clients_info) != 1:
                    string = string + clients_name[i] + ", "
                else:
                    string = string + clients_name[i]


            # send him the names of everyone
            s.sendto(string, sender_info)
            if not not clients_info:
                # send him the names of everyone
                s.sendto("", sender_info)
            # add him to the list
            clients_info.append(sender_info)
            clients_name.append(data2[1])
            clients_msg.append([])
        else:
            s.sendto("illegal request", sender_info)
            # client stop receiving
            s.sendto("", sender_info)

    else:
        if data2[0] == "2" and len(data2) > 1:
            # save his msg at all clients' lists
            for i in range(len(clients_info)):
                if i != client:
                    clients_msg[i].append(clients_name[client] + ": " + data2[1])
            for y in clients_msg[client]:
                s.sendto(y, sender_info)
            while not not clients_msg[client]:
                clients_msg[client].pop()
            # client stop receiving
            s.sendto("", sender_info)

        elif data2[0] == "3" and len(data2) > 1:
            # save this msg at all clients' lists
            for i in range(len(clients_info)):
                clients_msg[i].append(clients_name[client] + " changed his name to " + data2[1])
            for y in clients_msg[client]:
                s.sendto(y, sender_info)
            while not not clients_msg[client]:
                clients_msg[client].pop()
            # client stop receiving
            s.sendto("", sender_info)
            # change his name
            clients_name[client] = data2[1]

        elif data2[0] == "4" and len(data2) == 1:
            # save this msg at all clients' lists
            for i in range(len(clients_info)):
                if i != client:
                    clients_msg[i].append(clients_name[client] + " has left the group")
            # client stop receiving
            s.sendto("", sender_info)
            # dlt all the data of this client
            clients_name.pop(client)
            clients_msg.pop(client)
            clients_info.pop(client)

        elif data2[0] == "5" and len(data2) == 1:
            for y in clients_msg[client]:
                s.sendto(y, sender_info)
            while not not clients_msg[client]:
                clients_msg[client].pop()
            # client stop receiving
            s.sendto("", sender_info)

        else:
            s.sendto("illegal request", sender_info)
            # client stop receiving
            s.sendto("", sender_info)
