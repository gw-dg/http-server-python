import socket

def extract_path(request):
    lines = request.splitlines()
    response_body = ""
    for i in range(len(lines)):
        if lines[i].find("User-Agent") != -1 :
            response_body = lines[i]
            break;
    resp_cont = response_body.split();
    return resp_cont[1];
    
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        content = extract_path(request)
        length = len(content)
        status = "200 OK"
        response = "HTTP/1.1 " + status+ "\r\nContent-Type: text/plain\r\nContent-Length: " + str(length)+"\r\n\r\n"+content
        
        
        client_socket.sendall(response.encode('utf-8'))

        
    
        client_socket.close()



if __name__ == "__main__":
    main()
