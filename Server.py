#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:45:31 2020

@author: matt
"""
# Server for tcp connected chat application

import socket
import threading
from socket import gethostbyname

# list of all client connections
CLIENT_LIST = []

# establish server connection through tcp connection
s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = gethostbyname('10.0.0.246')
PORT = 1234
s_socket.bind((HOST, PORT))

s_socket.listen(1)
print('Chat server started on {HOST} : {PORT}'.format(HOST=HOST, PORT=PORT))


# accepts clients connection to the server
def accept_client():
    while True:
        # receive client connection request
        c_socket, c_address = s_socket.accept()
        uname = c_socket.recv(1024)
        CLIENT_LIST.append((uname, c_socket))

        print('{} is now connected'.format(c_address))

        new_user_msg = ('{} has joined the chat'.format(uname.decode('utf-8')))

        broadcast_thread = threading.Thread(target=broadcast_message, args=[uname, c_socket, c_address])
        broadcast_thread.start()

        # send join message to other connected clients
        server_message(c_socket, new_user_msg)


# handles all base work for determining what message needs to be sent to clients
def broadcast_message(uname, c_socket, c_address):
    while True:
        try:
            data = c_socket.recv(1024)
            # if there is data to be sent
            if data:
                # if the client happened to send end (quit message)
                if data.decode('utf-8') == 'end':

                    # run leave steps
                    client_left(c_socket, uname, c_address)
                    CLIENT_LIST.remove((uname, c_socket))
                    break

                else:

                    # sends client message to client message method
                    print("{} has spoken in the chat".format(c_address))
                    client_message(c_socket, uname, data)

            else:
                # if no data - user left
                client_left(c_socket, uname, c_address)
                CLIENT_LIST.remove((uname, c_socket))
                break

        except Exception as x:

            print(x.message)
            break


# method for sending clients the leave message
def client_left(c_socket, uname, c_address):
    leave_message = ("{} has left the chat".format(c_address))

    print(leave_message)

    leave_message = ("{} has left the chat".format(uname.decode('utf-8')))

    server_message(c_socket, leave_message)


# messages coming directly from the server to the clients
def server_message(c_socket, msg):
    # for every client in the client list
    for client in CLIENT_LIST:
        # send message if and only if client is not the one doing the action
        if client[1] != c_socket:
            servers_message = ('SERVER > {}'.format(msg))
            client[1].send(servers_message.encode('utf-8'))


# messages coming from 1 client being sent to all other clients
def client_message(c_socket, uname, msg):
    for client in CLIENT_LIST:

        # send message if and only if client is not the one doing action
        if client[1] != c_socket:
            updated_msg = ('{user} > {msg}'.format(user=uname.decode('utf-8'), msg=msg.decode('utf-8')))
            client[1].send(updated_msg.encode('utf-8'))


# method to cleanly have threads in
def start_server():
    accept_thread = threading.Thread(target=accept_client)
    accept_thread.start()


start_server()
