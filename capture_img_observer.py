import sys
import os

import subprocess

def get_files(p):
    p = subprocess.Popen(['ls', '-t', p], stdout=subprocess.PIPE)
    res = p.stdout.read()
    return res.decode('utf-8').split("\n")

# dataset name
path = "./datasets/" + sys.argv[2]

# fail or success
path = path + "/" + sys.argv[1] + "_" 


from http.server import BaseHTTPRequestHandler, HTTPServer
import cv2 as cv

hostName = "0.0.0.0"
serverPort = 9000

width = 640
height = 480

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if ("/raw" in self.path):
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            data = get_files(path + "raw/")
            img = cv.imread(path + "raw/" + data[0])
            img = cv.resize(img, (width, height), interpolation = cv.INTER_AREA)
            self.wfile.write(cv.imencode('.jpg', img)[1].tobytes())
        elif ("/filtered" in self.path):
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            data = get_files(path + "filtered/")
            with open(path + "filtered/" + data[0], 'rb') as f:
                self.wfile.write(f.read())
                f.close()
        elif ("/masked" in self.path):
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            data = get_files(path + "masked/")
            with open(path + "masked/" + data[0], 'rb') as f:
                self.wfile.write(f.read())
                f.close()
        elif (self.path == "/df"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            p = subprocess.Popen("df", stdout=subprocess.PIPE)
            res = p.stdout.read()
            self.wfile.write(res)
        elif (self.path == "/psaux"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            p = subprocess.Popen(["ps", "aux" , "--sort=-pcpu"], stdout=subprocess.PIPE)
            res = p.stdout.read()
            self.wfile.write(res)
        elif (self.path == "/curr"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            res = get_files(path + "raw/")
            self.wfile.write(str.encode(res[0]))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('observer.html', 'rb') as f:
                self.wfile.write(f.read())
                f.close()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")