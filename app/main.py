import socket
import os
import sys

# Function to extract path from request and handle different endpoints
def extract_path(request, directory):
    data = request.split("\r\n")
    path = data[0].split(" ")[1]
    
    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo"):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
    elif path.startswith("/user-agent"):
        content = data[2].split(" ")[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    elif path.startswith("/files/"):
        filename = path.split("/")[-1]
        filepath = os.path.join(directory, filename)
        
        if os.path.exists(filepath) and os.path.isfile(filepath):
            content_length = os.path.getsize(filepath)
            with open(filepath, 'rb') as file:
                file_content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {content_length}\r\n\r\n{file_content.decode('utf-8')}"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    
    return response

# Main function to run the server
def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--directory':
        print("Usage: python server.py --directory /path/to/files")
        return
    
    directory = sys.argv[2]
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        response = extract_path(request, directory)
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    main()
