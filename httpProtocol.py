import os
from typing import List

"""
HTTP protocol based on 1.1 version, using socket
"""

BANDWIDTH = 1024


class Request:

    METHODS = ["GET"]

    def __init__(self, soc):
        self.data = None
        self.receive_request(soc)
        self.request_line = []
        self.get_request_line()
        self.headers = None
        if self.is_valid():
            self.request_method = self.request_line[0]
            self.file_url = (self.request_line[1])[1:]
            self.get_headers()
        else:
            print(self.request_line)
            raise Exception("Invalid request")

    def receive_request(self, soc):
        self.data = soc.recv(BANDWIDTH).decode()

    def get_request_line(self):
        request_lines = self.data.split("\n")
        self.request_line = request_lines[0].split(" ")

    def is_valid(self):
        try:
            if not is_in_list(self.request_line[0], self.METHODS):
                return False
            if self.request_line[2] != "HTTP/1.1\r":
                return False
            return True
        except Exception as e:
            print(e)
        return False

    def get_headers(self):
        request_lines = self.data.split("\n")[1:-2]
        self.headers = {}
        for header in request_lines:
            header_data = header.split(":")
            self.headers[header_data[0]] = header_data[1]

    def __str__(self):
        return self.data


def is_in_list(item, lst: List):
    for i in lst:
        if i == item:
            return True
    return False


class Response:

    CODE_TO_STATEMENT = {200: "OK", 404: "Not Found"}

    def __init__(self, request: Request):
        self.status = None
        self.statement = None
        self.file_url = request.file_url
        self.file_data = None
        self.content_type = None
        if self.is_file_valid():
            self.set_content_type()
            self.status = 200
            self.statement = self.CODE_TO_STATEMENT[self.status]
            self.get_file_data()
        else:
            self.not_found_response()

    def not_found_response(self):
        self.status = 404
        self.statement = self.CODE_TO_STATEMENT[self.status]
        self.file_data = "<html>" \
                         " <body>" \
                         "     <h1>{self.status} {self.statement}</h1>" \
                         " </body>" \
                         "</html>"
        self.content_type = "text/html; charset=utf-8"

    def generate_response(self):
        headers = f"HTTP/1.1 {self.status} {self.statement}\r\n" \
               f"Content-Length: {len(self.file_data)}\r\n" \
               f"Content-Type: {self.content_type}\r\n" \
               f"\r\n"
        response = headers.encode()
        return response.__add__(self.file_data)

    def set_content_type(self):
        file_type = self.file_url.split(".")[-1]
        print(file_type)
        if file_type == "css":
            self.content_type = "text/css"
        elif file_type == "js":
            self.content_type = "text/javascript; charset=UTF-8"
        elif file_type == "jpg":
            self.content_type = "image/jpeg"
        elif file_type == "txt" or file_type == "html":
            self.content_type = "text/html; charset=utf-8"
        else:
            raise Exception("Unsupported file type")

    def get_file_data(self):
        with open(self.file_url, 'rb') as file:
            self.file_data = bytearray(file.read())

    def send_to_client(self, soc):
        data = self.generate_response()
        soc.sendall(data)

    def is_file_valid(self):
        if self.file_url == "":
            print("i was here")
            self.file_url = "index.html"
        return os.path.exists(self.file_url)
