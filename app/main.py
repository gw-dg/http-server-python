import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    #server_socket.accept() 
    while True:
        client_socket, client_address = server_socket.accept()
        response = "HTTP/1.1 200 OK\r\n\r\n"
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()



if __name__ == "__main__":
    main()
