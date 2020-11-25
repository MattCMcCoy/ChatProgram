#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:45:43 2020

@author: matt
"""

import socket, threading

c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


IP = '10.0.0.246'
PORT = 1234
c_socket.connect((IP, PORT))     
print('You have been connected to {IP} on {PORT}'.format(IP = IP, PORT = PORT))
uname = input('Username: ').encode('utf-8')
c_socket.send(uname)


def send_message():
    while True:
        sent_message = input().encode('utf-8')
        c_socket.send(sent_message)

def receive_message():
    while True:
        recieved_message = c_socket.recv(1024)
        recieved_message = recieved_message.decode('utf-8')
        print((recieved_message))

if __name__ == "__main__":   
   
    
    send_thread = threading.Thread(target = send_message)
    recieve_thread = threading.Thread(target = receive_message)
    
    send_thread.start()  
    recieve_thread.start()