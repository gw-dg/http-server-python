import socket

def extract_path(request):
    data = request.split("\r\n")
    path = data[0].split(" ")[1]
    response = ""
    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo"):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
    elif path.startswith("/user-agent"):
        content = data[2].split(" ")[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    else :
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    return response
    
    
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        response = extract_path(request)
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()



if __name__ == "__main__":
    main()
