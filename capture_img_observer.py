import sys

path = sys.argv[1]

import subprocess

def get_files():
    p = subprocess.Popen(['ls', '-t', path], stdout=subprocess.PIPE)
    res = p.stdout.read()
    return res.decode('utf-8').split("\n")

data = get_files()

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "0.0.0.0"
serverPort = 9000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == "/image"):
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            data = get_files()
            with open(path + data[0], 'rb') as f:
                self.wfile.write(f.read())
                f.close()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Progress monitor</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<img style=\"width: 100%\" src=\"/image\">", "utf-8"))
            self.wfile.write(bytes("<script>setTimeout(() => {document.location.reload()}, 30000)</script>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")