import socket
import httpProtocol

IP = "0.0.0.0"
PORT = 80
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))

print("Server is up and running")


def handle_client(soc, addr):
    try:
        print(f"Connected to {addr}")
        client_request = httpProtocol.Request(soc)
        print(client_request)
        while True:
            response = httpProtocol.Response(client_request)
            response.send_to_client(soc)
            client_request.__init__(soc)
    except Exception as e:
        print(e)
    soc.close()
    print("closed")


def listen_to_client():
    server_socket.listen()
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    handle_client(client_socket, client_address)


def main():
    while True:
        listen_to_client()


if __name__ == '__main__':
    main()
