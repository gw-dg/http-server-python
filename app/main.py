import socket

def extract_path(request):
    lines = request.splitlines()
    if lines:
        request_line = lines[0].strip()
        parts = request_line.split()
        if len(parts)>=2:
            return parts[1]
    return None;
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        path = extract_path(request)
        content = ""
        length = 0
        status = "200 OK"
        if extract_path(request) != None:
            a = extract_path(request).split('/')
            
            if len(extract_path(request))>1: 
                if a[1] != "echo" : 
                    status = "404 NOT FOUND"
                else :
                    content = a[2]
                    length = len(content)
        response = ""
        if status == "200 OK":
            response = "HTTP/1.1 " + status+ "\r\nContent-Type: text/plain\r\nContent-Length: " + str(length)+"\r\n\r\n"+content
        else :
            response = "HTTP/1.1 " + status+"\r\n\r\n"
        
        client_socket.sendall(response.encode('utf-8'))

        
    
        client_socket.close()



if __name__ == "__main__":
    main()
