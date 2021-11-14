#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:45:43 2020

@author: matt
"""

# Client for tcp connected chat application

import socket
import sys
import threading

# setting up client connections to server through tcp
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = '10.0.0.246'
PORT = 1234
c_socket.connect((IP, PORT))
print('You have been connected to {IP} on {PORT}'.format(IP=IP, PORT=PORT))
uname = input('Username: ').encode('utf-8')
c_socket.send(uname)


# user inputs message and it gets sent to the server
def send_message():
    while True:
        sent_message = input().encode('utf-8')

        # closes connection if user types end
        if sent_message.decode('utf-8') == 'end':
            c_socket.send(sent_message)
            c_socket.close()
            sys.exit()

        c_socket.send(sent_message)


# user receives message from server which came from another client
def receive_message():
    while True:
        try:
            recieved_message = c_socket.recv(1024)
            recieved_message = recieved_message.decode('utf-8')
            print(recieved_message)
        # closes connection if any type of exception occurs
        except Exception:
            c_socket.close()
            sys.exit()


# threads method to run the threads cleanly
def start_client():
    send_thread = threading.Thread(target=send_message)
    send_thread.start()
    recieve_thread = threading.Thread(target=receive_message)
    recieve_thread.start()


start_client()
