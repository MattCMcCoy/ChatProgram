#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:45:31 2020

@author: matt
"""
import socket, threading
from socket import gethostbyname
CLIENT_LIST = []


s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = gethostbyname('10.0.0.246')
PORT = 1234
s_socket.bind((HOST, PORT))

   
s_socket.listen(1)
print('Chat server started on {HOST} : {PORT}'.format(HOST = HOST, PORT = PORT))

def accept_client():
    while True:
           
        c_socket, c_address = s_socket.accept()
        uname = c_socket.recv(1024)
        CLIENT_LIST.append((uname, c_socket))
        print('{} is now connected'.format(uname.decode('utf-8')))
        client_thread = threading.Thread(target = broadcast_message, args=[uname, c_socket])
        client_thread.start()

def broadcast_message(uname, c_socket):
    while True:
        try:
            data = c_socket.recv(1024)
            if data:
                print ("{} has spoken in the chat".format(uname.decode('utf-8')))
               
                send_message(c_socket, uname, data)
                
        except Exception as x:
            print(x.message)
            break

def send_message(c_socket, uname, msg):
    
    for client in CLIENT_LIST:
        if client[1] != c_socket:
            updated_msg = ('{user} > {msg}'.format(user = uname.decode('utf-8'), msg = msg.decode('utf-8')) )
            client[1].send((updated_msg).encode('utf-8'))
            
            
     
if __name__ == "__main__":    
   

    thread_ac = threading.Thread(target = accept_client)
    thread_ac.start()

   