# messages can be sent with any post request formatted as such: {"author":"<author>", "message":"<message>"}
# member list formatted as: ip,nick,rsa public key

# TODO: exit function closes file
# TODO: cute curses frontend
# TODO: e2e encryption
# TODO: fix logging

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from threading import Thread
import json
import socket
# make sure the normies pip install these
import requests

ip = socket.gethostbyname(socket.gethostname())
port = 8000
name = "<nick>"
# must create a member list before running
members = open("members.txt", "r")
log = open("message_log.txt", "a")

class bcpServer(BaseHTTPRequestHandler):

    def do_POST(self):
        global name
        # updates message_log with contents of message

        content_length = int(self.headers["Content-Length"])
        raw = self.rfile.read(content_length)
        parsed = json.loads(raw.decode("utf-8"))

        # required for response to be recognized as valid
        self.send_response(200)
        self.end_headers()

        response = BytesIO()

        log.write("[RECEIVED] AUTHOR " + parsed["author"] + " SENT \"" + parsed["message"] + "\"")

        print(parsed["author"] + ": " + parsed["message"])
        response.write(b"[SENT] message received by recipient " + name.encode("UTF-8"))

        # wfile output stream for response to client
        self.wfile.write(response.getvalue())

    def log_message(self, format, *args):
        # silence do_POST

        return

def send_message():
    while True:
        message = input()
        for member in members:
            reply = requests.post(member, json={"author": name, "message": message})

            log.write(reply.text)
        members.seek(0)

def start_server():
    server_instance = HTTPServer((ip, port), bcpServer)
    server_instance.serve_forever()

def main():

    # threading is absolute magic
    # https://www.shanelynn.ie/using-python-threading-for-multiple-results-queue/
    threads = []
    server_process = Thread(target=start_server)
    server_process.start()
    threads.append(server_process)

    message_process = Thread(target=send_message)
    message_process.start()
    threads.append(message_process)

    for process in  threads:
        process.join()
    log.close()


if __name__ == "__main__":
    main()
