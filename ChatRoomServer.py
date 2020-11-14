#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:59:17 2020

@author: matt
"""

import socket
import select



IP = socket.gethostname()
PORT = 12345

# Create a socket (TCP)
s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s_socket.bind((IP, PORT))


s_socket.listen()

# List of sockets and clients
socket_list = [s_socket]
c_list = {}
print('Awaiting Connections....')
def receive_message(client_socket):

    try:

        
        message_header = client_socket.recv(10)

       
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        
        return False

#remove exited clients
def cleanup_list(notified_socket):
    
    try:
        print('Closed connection from: {}'.format(c_list[notified_socket]['data'].decode('utf-8')))

        # Remove from list for socket.socket() and users
        socket_list.remove(notified_socket)
        del c_list[notified_socket]
    except:
        return False

#sends to all connected clients
def broadcast_message():
    for c_socket in c_list:
        
                
        if c_socket != notified_socket:
            
            c_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
   
while True:

   
    read, _, _ = select.select(socket_list, [], [])


    
    for notified_socket in read:

        # If notified socket is a server socket accept connection
        if notified_socket == s_socket:

            c_socket, c_address = s_socket.accept()
            username = receive_message(c_socket)


            # Add accepted socket to socket_list & save username
            socket_list.append(c_socket)
            c_list[c_socket] = username

            print('Accepted a new connection from: {} ({}:{})'.format(username['data'].decode('utf-8'), *c_address))
            
        else:

            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup the list
            if message is False:
               
                cleanup_list(notified_socket)

                continue

            # Get user by notified socket, so we know who sent the message
            user = c_list[notified_socket]

            print('Received a message from ' + user["data"].decode("utf-8") + ': ' + message["data"].decode("utf-8"))
            
           
            broadcast_message()

   