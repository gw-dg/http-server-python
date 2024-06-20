import socket
import sys
import gzip
import io

# Function to extract path from request and handle different endpoints
def extract_path(request):
    data = request.split("\r\n")
    request_type = data[0].split(" ")[0]
    path = data[0].split(" ")[1]
    
    # Extract Accept-Encoding header if it exists
    accept_encoding = None
    for line in data:
        if line.startswith("Accept-Encoding:"):
            accept_encoding = line.split(": ")[1]
            break

    if request_type == "GET":
        if path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo"):
            response_body = path[6:]
            headers = {
                "Content-Type": "text/plain"
            }

            # Handle gzip compression
            if accept_encoding and "gzip" in accept_encoding:
                # Compress the response body using gzip
                out = io.BytesIO()
                with gzip.GzipFile(fileobj=out, mode="w") as gz:
                    gz.write(response_body.encode('utf-8'))
                compressed_body = out.getvalue()
                headers["Content-Encoding"] = "gzip"
                headers["Content-Length"] = str(len(compressed_body))
                response_body = compressed_body
            else:
                headers["Content-Length"] = str(len(response_body))

            headers_formatted = "\r\n".join(f"{key}: {value}" for key, value in headers.items())
            response = f"HTTP/1.1 200 OK\r\n{headers_formatted}\r\n\r\n"
            response = response + response_body if isinstance(response_body, bytes) else response + response_body

        # elif path.startswith("/echo"):
        #     response_body = path[6:]
        #     headers = {
        #         "Content-Type": "text/plain",
        #         "Content-Length": str(len(response_body))
        #     }

        #     # Handle gzip compression
        #     if accept_encoding and "gzip" in accept_encoding:
        #         headers["Content-Encoding"] = "gzip"
            
        #     headers_formatted = "\r\n".join(f"{key}: {value}" for key, value in headers.items())
        #     response = f"HTTP/1.1 200 OK\r\n{headers_formatted}\r\n\r\n{response_body}"
        
        elif path.startswith("/user-agent"):
            content = data[2].split(" ")[1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
        
        elif path.startswith("/files"):
            directory = sys.argv[2]
            filename = path[7:]
            try:
                with open(f"/{directory}/{filename}", "r") as f:
                    body = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
            except Exception as e:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n"
        
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    
    elif request_type == "POST":
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
