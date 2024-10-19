import socket
import threading

# Client settings
HOST = '127.0.0.1'  # Matches server's IP address
PORT = 12346

# Initialize socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Function to receive messages from server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

# Function to send messages to server
def send_message():
    while True:
        message = input("Enter message or type 'sendfile <filename>' to share a file: ")
        if message.startswith("sendfile"):
            filename = message.split(" ", 1)[1].strip('"')  # Strip any extra quotes
            try:
                client_socket.send(f"FILE {filename}".encode())
                with open(filename, "rb") as f:
                    while (file_data := f.read(1024)):
                        client_socket.send(file_data)
                client_socket.send(b"DONE")
            except FileNotFoundError:
                print("File not found.")
            except OSError as e:
                print(f"Error: {e}")
        else:
            client_socket.send(message.encode())


# Start threads
threading.Thread(target=receive_messages).start()
send_message()
