# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 09:49:50 2024

@author: mostafa modified with mohamed Elrashidy
"""

import socket
import threading
import ast


def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive the length of the incoming message
            message_length = int.from_bytes(client_socket.recv(4), byteorder='big')
            # Receive the actual message with the calculated length
            data = client_socket.recv(message_length).decode('utf-8')
            if not data:
                break
            print(f"Received from {client_address}: {data}")

            # Extract the recipient client's address from the message
            recipient_address, message = data.split(':', 1)

            # Find the recipient client's socket
            recipient_socket = None
            for client in clients:
                """
                The ast.literal_eval() function safely evaluates a string containing a Python literal 
                (such as a tuple, list, dictionary, number, or string) and returns the corresponding Python 
                object. It ensures that only literals are evaluated, preventing the execution of arbitrary code.
                """
                print(f"Client: {client[1]}")
                print(f"Recipient: {ast.literal_eval(recipient_address)}")
                if client[1] == ast.literal_eval(recipient_address): # or you can convert client[1] to str: if str(client[1]) == recipient_address
                    recipient_socket = client[0]
                    break
            print(f"Recipient socket: {recipient_socket}")
            if recipient_socket:
                # Send the message to the recipient client
                recipient_socket.send(message.encode('utf-8'))
            else:
                print(f"Recipient not found: {recipient_address}")

        except socket.error:
            break

    print(f"Connection closed with {client_address}")
    clients.remove((client_socket, client_address))
    client_socket.close()

def start_server():
    host = 'localhost'
    port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append((client_socket, client_address))
        print(f"Connected with {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == '__main__':
    clients = []
    start_server()