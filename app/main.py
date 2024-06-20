import socket
import os
import sys

# Function to extract path from request and handle different endpoints
def extract_path(request):
    data = request.split("\r\n")
    request_type = data[0].split(" ")[0]
    path = data[0].split(" ")[1]
    
    if request_type == "GET":
        if path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo"):
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
        elif path.startswith("/user-agent"):
            content = data[2].split(" ")[1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
        elif path.startswith("/files"):
            directory = sys.argv[2]
            filename = path[7:]
            print(directory, filename)
            try:
                with open(f"/{directory}/{filename}", "r") as f:
                    body = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
            except Exception as e:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    elif request_type == "POST" :
        if path.startswith("/files"):
            directory = sys.argv[2]
            filename = path.split("/")[2]
            content = data[-1]
            with open(f"/{directory}/{filename}", "w") as f:
                f.write(content)
            response = "HTTP/1.1 201 Created\r\n\r\n"
            
    
    return response

# Main function to run the server
def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        response = extract_path(request)
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    main()
