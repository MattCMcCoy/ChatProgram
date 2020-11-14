#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:58:14 2020

@author: matt
"""

import socket




IP = socket.gethostname()
PORT = 12345

username = input("Username: ").encode('utf-8')
username_header = f"{len(username):<{10}}".encode('utf-8')

# create a TCP socket
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((IP, PORT))
c.setblocking(False)

# sends username and header
c.send(username_header + username)


#Receive and decode username and message   
def recieveMessage():
   
    while True:

            username_header = c.recv(10)
            username_length = int(username_header.decode('utf-8').strip())
            username = c.recv(username_length).decode('utf-8')

            msg_header = c.recv(10)
            msg_length = int(msg_header.decode('utf-8').strip())
            msg = c.recv(msg_length).decode('utf-8')
            print(f'{username} > {msg}') 
    

while True:
   
    # Wait for user to input a message
    msg = input(f'{username.decode()} > ')

    # If message isnt empty send it
    if msg:
        
        msg = msg.encode('utf-8')
        msg_header = f"{len(msg):<{10}}".encode('utf-8')
        c.send(msg_header + msg)
        
        try:
            recieveMessage()
          
        
        except:
            continue
    

