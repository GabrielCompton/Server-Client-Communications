import socket
import threading
import os

# Server settings
HOST = '127.0.0.1'  # localhost
PORT = 12346

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

clients = []

# Function for client communication
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith("FILE"):
                filename = message.split(" ")[1]
                with open(f"received_{filename}", "wb") as f:
                    while True:
                        file_data = client_socket.recv(1024)
                        if file_data == b"DONE":
                            break
                        f.write(file_data)
                broadcast(f"{filename} received from client")
            else:
                broadcast(message)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

# Function to send message to all clients
def broadcast(message):
    for client in clients:
        client.send(message.encode())


print("Server is running and waiting for clients to connect...")
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"Connection from {client_address}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
