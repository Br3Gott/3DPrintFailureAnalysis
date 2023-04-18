import sys
import numpy as np

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
from tensorflow.tensorflow_identify import Identify
import datetime

date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
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
        elif (self.path == "/tf"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            res = get_files(path + "filtered/")
            image = cv.imread(path + "filtered/" + res[0])
            ident = Identify.run(image, verbose=True)
            self.wfile.write(str.encode("Fail: {:.2f} Success: {:.2f}".format(ident[0], ident[1])))
            
            # Write to log file
            class_names = ["Fail", "Success"]
            if ident[np.argmax(ident)] > 0.60 and np.argmax(ident) == 0:
                threshold = "Below"
            else:
                threshold = "Passing"
            with open('tflog' + date + '.txt', 'a') as log:
                log.write("{} [{:.2f}, {:.2f}] Threshold: {} ({})\n".format(class_names[np.argmax(ident)], ident[0], ident[1], threshold, path + "filtered/" + res[0]))
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