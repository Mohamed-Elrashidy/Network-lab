import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            print(data)
        except socket.error:
            break

def send_message(sock):
    while True:
        message = input()
        recipient = input("Enter recipient address (host:port): ")
        data = f"{recipient}:{message}"
        # Prefix the message with its length
        message_length = len(data).to_bytes(4, byteorder='big')
        sock.sendall(message_length)
        sock.sendall(data.encode('utf-8'))

def start_chat():
    host = 'localhost'
    port = 8000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"Connected to {host}:{port}")
    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_message, args=(sock,))
    send_thread.start()

if __name__ == '__main__':
    start_chat()
